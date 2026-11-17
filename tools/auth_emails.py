"""The sign-in emails Claritia's sign-in service (GoTrue on the VPS, db.tryclaritia.com) sends.

Writes email/auth/<name>.html. The sign-in service loads each one from https://tryclaritia.com/email/auth/<name>.html
(GOTRUE_MAILER_TEMPLATES_* in its settings), so a push to main updates the emails. Header art: assets/email/, drawn
from an HTML page and saved at 2x. The {{ .Name }} parts are filled in by the sign-in service when it sends.

Run: python3 tools/auth_emails.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "email" / "auth"
CDN = "https://tryclaritia.com/assets/email"

FONT = "Inter,ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

# name, subject, preheader, art, title, lead (html), button, code (with code_line when it sits under a button),
# expiry line, extra block (html), footer reason
EMAILS = [
    dict(
        name="confirm-signup", subject="Welcome to Claritia: confirm your email",
        pre="One click and your Claritia account is ready.",
        art="welcome", title="Welcome to Claritia",
        lead='Confirm <b style="color:#171717;font-weight:600">{{ .Email }}</b> and your account is ready. Forms, meetings and email marketing, all in one place.',
        button="Confirm my email", url="{{ .ConfirmationURL }}", expiry="Works once, for the next hour",
        code="{{ .Token }}", code_line="Or type this code on the sign-in page:",
        next=[("Build your first form", "Describe it in a sentence or pick one of 840 templates."),
              ("Connect your calendar", "Google Calendar or Outlook, in one click.")],
        reason="You got this email because someone signed up for Claritia with this address. If it wasn't you, you can ignore it.",
    ),
    dict(
        name="magic-link", subject="Your Claritia sign-in link",
        pre="Tap the button to sign in. No password needed.",
        art="signin", title="Sign in to Claritia",
        lead='Here is your sign-in link for <b style="color:#171717;font-weight:600">{{ .Email }}</b>. Tap the button and you\'re in.',
        button="Sign in to Claritia", url="{{ .ConfirmationURL }}", expiry="Works once, for the next hour",
        code="{{ .Token }}", code_line="Or type this code on the sign-in page:",
        reason="You got this email because someone asked to sign in to Claritia with this address. If it wasn't you, you can ignore it. Your account is safe.",
    ),
    dict(
        name="reset-password", subject="Reset your Claritia password",
        pre="Pick a new password for your Claritia account.",
        art="reset", title="Pick a new password",
        lead="Someone asked to reset the password for your Claritia account. Tap the button to choose a new one.",
        button="Choose a new password", url="{{ .ConfirmationURL }}", expiry="Works once, for the next hour",
        reason="If you didn't ask for this, you can ignore this email. Your password stays the same.",
    ),
    dict(
        name="invite", subject="You're invited to Claritia",
        pre="Your team uses Claritia for forms, meetings and email. Join them.",
        art="invite", title="You're invited to Claritia",
        lead="Your team uses Claritia to capture leads, book meetings and follow up by email. Accept the invite to join them.",
        button="Accept the invite", url="{{ .ConfirmationURL }}", expiry="Works once, for the next hour",
        reason="You got this email because a Claritia user invited this address. If you weren't expecting it, you can ignore it.",
    ),
    dict(
        name="email-change", subject="Confirm your new email for Claritia",
        pre="One click to move your Claritia account to a new email.",
        art="change", title="Confirm your new email",
        lead='Your Claritia account is moving from <b style="color:#171717;font-weight:600">{{ .Email }}</b> to <b style="color:#171717;font-weight:600">{{ .NewEmail }}</b>. Tap the button to confirm.',
        button="Confirm new email", url="{{ .ConfirmationURL }}", expiry="Works once, for the next hour",
        reason="If you didn't ask for this change, ignore this email and write to hello@tryclaritia.com. Your account keeps its current email.",
    ),
    dict(
        name="reauthentication", subject="Your Claritia code",
        pre="Use this code to confirm it's you.",
        art="code", title="Confirm it's you",
        lead="Enter this code in Claritia to finish your change.",
        code="{{ .Token }}", expiry="Works once, for the next hour",
        reason="If you didn't ask for a code, you can ignore this email. Nothing changes without it.",
    ),
]

def button(label, url):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td bgcolor="#333333" style="border-radius:999px;background:#333333">
                            <a href="{url}" style="display:inline-block;padding:13px 24px;font-size:15px;line-height:18px;font-weight:500;letter-spacing:-0.01em;color:#ffffff;text-decoration:none;border-radius:999px;border:1px solid #1f1f1f">{label}&nbsp;&nbsp;&rarr;</a>
                          </td>
                        </tr>
                      </table>"""

def code_box(code):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tr>
                          <td align="center" style="padding:18px 12px;border-radius:12px;background:#f2faf6;border:1px solid #c9eadb;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:32px;line-height:36px;font-weight:600;letter-spacing:0.28em;color:#0f0f0f">{code}</td>
                        </tr>
                      </table>"""

def next_steps(items):
    rows = ""
    for i, (h, t) in enumerate(items, 1):
        rows += f"""
                        <tr>
                          <td width="28" valign="top" style="padding:12px 0 0">
                            <div style="width:22px;height:22px;border-radius:7px;background:#e3f4ec;color:#086444;font-size:12px;line-height:22px;font-weight:600;text-align:center">{i}</div>
                          </td>
                          <td valign="top" style="padding:12px 0 0 6px">
                            <p style="margin:0;font-size:14px;line-height:20px;font-weight:500;color:#171717">{h}</p>
                            <p style="margin:2px 0 0;font-size:13px;line-height:19px;color:#737373">{t}</p>
                          </td>
                        </tr>"""
    return f"""<tr>
                    <td style="padding:0 28px">
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #ebebeb;font-size:0;line-height:0">&nbsp;</td></tr></table>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:18px 28px 24px">
                      <p style="margin:0;font-size:12px;line-height:16px;font-weight:500;color:#a3a3a3">After that</p>
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}
                      </table>
                    </td>
                  </tr>"""

def fallback(url):
    return f"""<tr>
                    <td style="padding:0 28px">
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #ebebeb;font-size:0;line-height:0">&nbsp;</td></tr></table>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:16px 28px 22px">
                      <p style="margin:0 0 4px;font-size:12px;line-height:1.5;color:#737373">Button not working? Paste this link into your browser:</p>
                      <p style="margin:0;font-size:12px;line-height:1.55;color:#a3a3a3;word-break:break-all"><a href="{url}" style="color:#a3a3a3;text-decoration:underline">{url}</a></p>
                    </td>
                  </tr>"""

def code_line(text):
    return f"""<p style="margin:22px 0 10px;font-size:13px;line-height:18px;color:#737373">{text}</p>"""

def page(e):
    if e.get("url"):
        action = button(e["button"], e["url"])
        if e.get("code"):
            action += "\n                      " + code_line(e["code_line"]) + "\n                      " + code_box(e["code"])
    else:
        action = code_box(e["code"])
    extra = next_steps(e["next"]) if e.get("next") else ""
    tail = fallback(e["url"]) if e.get("url") else ""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="light only" />
    <meta name="supported-color-schemes" content="light" />
    <meta name="robots" content="noindex" />
    <title>{e["subject"]}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  </head>
  <!-- Written by tools/auth_emails.py in perceptric/claritia-site. Edit the script, not this file. Subject: {e["subject"]} -->
  <body style="margin:0;padding:0;background:#fafaf5;font-family:{FONT};-webkit-font-smoothing:antialiased;color:#171717">
    <span style="display:none;max-height:0;max-width:0;overflow:hidden;opacity:0;color:transparent">{e["pre"]}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</span>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafaf5">
      <tr>
        <td align="center" style="padding:40px 16px 36px">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:520px">
            <tr>
              <td style="padding:0 4px 20px">
                <a href="https://tryclaritia.com" style="text-decoration:none"><img src="{CDN}/logo.png" width="87" height="28" alt="Claritia" style="display:block;border:0;width:87px;height:28px" /></a>
              </td>
            </tr>
            <tr>
              <td style="background:#ffffff;border-radius:18px;border:1px solid #ebebe4;padding:8px">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td style="font-size:0;line-height:0">
                      <img src="{CDN}/{e["art"]}.png" width="502" alt="" style="display:block;border:0;width:100%;max-width:502px;height:auto;border-radius:12px" />
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:30px 28px 26px">
                      <h1 style="margin:0 0 10px;font-size:28px;line-height:1.15;font-weight:500;letter-spacing:-0.035em;color:#0f0f0f">{e["title"]}</h1>
                      <p style="margin:0 0 26px;font-size:15px;line-height:1.6;color:#6c6c6d">{e["lead"]}</p>
                      {action}
                      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px">
                        <tr>
                          <td style="vertical-align:middle;padding-right:8px;font-size:0;line-height:0"><span style="display:inline-block;width:7px;height:7px;border-radius:99px;background:#0c8c5e"></span></td>
                          <td style="vertical-align:middle;font-size:13px;line-height:18px;color:#737373">{e["expiry"]}</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  {extra}
                  {tail}
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:22px 4px 0;font-size:12px;line-height:1.6;color:#a3a3a3">
                {e["reason"]}
              </td>
            </tr>
            <tr>
              <td style="padding:14px 4px 0;font-size:12px;line-height:1.6;color:#a3a3a3">
                <a href="https://tryclaritia.com" style="color:#737373;text-decoration:none;font-weight:500">Claritia</a>&nbsp;&middot;&nbsp;Forms, scheduling and email marketing in one app&nbsp;&middot;&nbsp;<a href="mailto:hello@tryclaritia.com" style="color:#737373;text-decoration:none">hello@tryclaritia.com</a>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for e in EMAILS:
        (OUT / f"{e['name']}.html").write_text(page(e))
        print(f"wrote email/auth/{e['name']}.html  ({e['subject']})")

if __name__ == "__main__":
    main()
