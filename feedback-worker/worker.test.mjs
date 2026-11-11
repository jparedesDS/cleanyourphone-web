import assert from "node:assert/strict";
import test from "node:test";

import worker from "./worker.js";

const ORIGIN = "https://cleanyourphone.org";

function memoryKv() {
  const values = new Map();
  return {
    async get(key) {
      return values.get(key) ?? null;
    },
    async put(key, value) {
      values.set(key, value);
    },
  };
}

function makeEnv(overrides = {}) {
  return {
    DISCORD_WEBHOOK_URL: "https://discord.test/webhook",
    IP_SALT: "test-salt",
    ALLOWED_ORIGIN: ORIGIN,
    FEEDBACK_KV: memoryKv(),
    ...overrides,
  };
}

function makeRequest(payload, init = {}) {
  return new Request("https://feedback.test/", {
    method: init.method ?? "POST",
    headers: {
      "Content-Type": "application/json",
      Origin: ORIGIN,
      "CF-Connecting-IP": "192.0.2.10",
      ...(init.headers ?? {}),
    },
    body: init.body ?? JSON.stringify(payload),
  });
}

function mockDiscord() {
  const calls = [];
  const original = globalThis.fetch;
  globalThis.fetch = async (url, init) => {
    calls.push({ url, payload: JSON.parse(init.body) });
    return new Response(null, { status: 204 });
  };
  return {
    calls,
    restore() {
      globalThis.fetch = original;
    },
  };
}

test("options returns CORS preflight", async () => {
  const response = await worker.fetch(makeRequest({}, { method: "OPTIONS" }), makeEnv());
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), ORIGIN);
});

test("valid feedback reaches Discord without exposing the webhook", async () => {
  const discord = mockDiscord();
  try {
    const response = await worker.fetch(
      makeRequest({
        kind: "feedback",
        message: "Please explain the review screen",
        checklist: "Phone: Test\nAndroid: 14",
        app_version: "CleanYourPhone app 0.2.1",
        website: "",
      }),
      makeEnv(),
    );
    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), { ok: true });
    assert.equal(discord.calls.length, 1);
    assert.equal(discord.calls[0].url, "https://discord.test/webhook");
    assert.equal(discord.calls[0].payload.embeds[0].title, "New feedback");
    assert.match(discord.calls[0].payload.embeds[0].description, /review screen/);
    assert.match(discord.calls[0].payload.embeds[1].description, /Phone: Test/);
    assert.deepEqual(discord.calls[0].payload.allowed_mentions, { parse: [] });
  } finally {
    discord.restore();
  }
});

test("honeypot silently accepts without calling Discord", async () => {
  const discord = mockDiscord();
  try {
    const response = await worker.fetch(
      makeRequest({ kind: "feedback", message: "spam", website: "bot" }),
      makeEnv(),
    );
    assert.equal(response.status, 200);
    assert.equal(discord.calls.length, 0);
  } finally {
    discord.restore();
  }
});

test("unknown kind is rejected", async () => {
  const response = await worker.fetch(
    makeRequest({ kind: "other", message: "hello" }),
    makeEnv(),
  );
  assert.equal(response.status, 400);
});

test("an empty message and checklist is rejected", async () => {
  const response = await worker.fetch(makeRequest({ kind: "feedback" }), makeEnv());
  assert.equal(response.status, 400);
});

test("missing webhook configuration returns 503", async () => {
  const response = await worker.fetch(
    makeRequest({ kind: "feedback", message: "hello" }),
    makeEnv({ DISCORD_WEBHOOK_URL: "" }),
  );
  assert.equal(response.status, 503);
});

test("the same IP is rate limited for five minutes", async () => {
  const discord = mockDiscord();
  const env = makeEnv();
  try {
    const first = await worker.fetch(
      makeRequest({ kind: "feedback", message: "one" }),
      env,
    );
    const second = await worker.fetch(
      makeRequest({ kind: "feedback", message: "two" }),
      env,
    );
    assert.equal(first.status, 200);
    assert.equal(second.status, 429);
    assert.equal(discord.calls.length, 1);
  } finally {
    discord.restore();
  }
});
