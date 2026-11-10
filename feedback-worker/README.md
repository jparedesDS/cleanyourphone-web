# CleanYourPhone feedback Worker

A small Cloudflare Worker that accepts a JSON feedback/checklist message and posts it to a private
Discord channel. The Discord webhook stays in a Worker secret; it is never shipped in the app or the
website.

## What it receives

```json
{
  "kind": "feedback",
  "message": "The review screen could explain ...",
  "checklist": "Phone: ...\nAndroid: ...\nBuild: ...",
  "contact": "optional Discord/GitHub/email",
  "app_version": "CleanYourPhone app 0.2.0 / CLI 0.3.2",
  "website": ""
}
```

`kind` is `feedback`, `bug` or `profile`. `message` or `checklist` is required. The `website` field is a
honeypot and must stay empty.

The Worker does not store the request body. It hashes the Cloudflare client IP with `IP_SALT` and
keeps only a five-minute rate-limit flag in KV. Serial numbers, IP addresses, IMEI and MAC addresses
must never be added to the checklist by the clients.

## Discord

1. Open the Discord server and the channel that should receive feedback.
2. **Channel settings → Integrations → Webhooks → New Webhook**.
3. Name it `CleanYourPhone`, copy the **Webhook URL**, and keep it private.

Do not put that URL in the website, the app, this repository or a chat message.

## Cloudflare dashboard

1. Go to **Workers & Pages → Create application → Create Worker**.
2. Name it `cleanyourphone-feedback` and deploy the starter.
3. Open **Edit code**, replace everything with the contents of `worker.js`, and deploy.
4. Go to **Storage & Databases → KV → Create namespace**. Name it
   `cleanyourphone-feedback-rate`.
5. Open the Worker → **Settings → Bindings → Add → KV namespace**:
   - Variable name: `FEEDBACK_KV`
   - KV namespace: `cleanyourphone-feedback-rate`
6. In **Settings → Variables and Secrets** add:
   - Secret `DISCORD_WEBHOOK_URL`: the Discord webhook from above.
   - Secret `IP_SALT`: a long random string. Generate one with a password manager.
   - Variable `ALLOWED_ORIGIN`: `https://jparedesds.github.io`
7. Deploy again and copy the public URL, for example:
   `https://cleanyourphone-feedback.your-subdomain.workers.dev`

The URL is public and can be shared. The webhook and `IP_SALT` are secrets.

## Wrangler CLI

```powershell
cd feedback-worker
npm install
npx wrangler login
npx wrangler kv namespace create FEEDBACK_KV
# Put the returned id in wrangler.toml.
npx wrangler secret put DISCORD_WEBHOOK_URL
npx wrangler secret put IP_SALT
npx wrangler deploy
```

Set `ALLOWED_ORIGIN` in `wrangler.toml` under `[vars]` if you use the CLI:

```toml
[vars]
ALLOWED_ORIGIN = "https://jparedesds.github.io"
```

## Test

After deploying, run this from PowerShell. Replace the URL with your Worker URL.

```powershell
$body = @{
  kind = "feedback"
  message = "Test from the CleanYourPhone setup"
  checklist = "Phone: test`nAndroid: test"
  website = ""
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://cleanyourphone-feedback.your-subdomain.workers.dev" `
  -ContentType "application/json" `
  -Body $body
```

Expected response: `ok : True`. The message should appear in Discord. If you send twice within five
minutes from the same IP, the second response is `429`.

## Security notes

- The Worker only accepts `POST` with JSON and caps the body at 16 KB.
- `message` is capped at 4000 characters and `checklist` at 6000.
- Discord mentions are disabled in the payload.
- Rate limiting is per hashed IP, five minutes, stored in KV.
- The Worker does not log or persist the message.
- CORS allows only `ALLOWED_ORIGIN`; the desktop app sends no Origin header and is not blocked by CORS.
