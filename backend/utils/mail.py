import logging
import os
from email.message import EmailMessage

from aiosmtplib import SMTP

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "TU NOTIFIER")
SITE_URL = os.getenv("FRONTEND_URL")

logger = logging.getLogger(__name__)


def _render_notice_row(notice: dict) -> str:
    return f"""
    <table
        role="presentation"
        width="100%"
        cellpadding="0"
        cellspacing="0"
        border="0"
        style="border-bottom:1px solid #e8e9ee;"
    >
        <tr>
            <td
                style="
                    width:8px;
                    padding:26px 14px 24px 0;
                    vertical-align:top;
                "
            >
                <div
                    style="
                        width:7px;
                        height:7px;
                        margin-top:6px;
                        border-radius:50%;
                        background:#7357e8;
                    "
                ></div>
            </td>

            <td style="padding:24px 0;">
                <a
                    href="{notice["link"]}"
                    style="
                        display:block;
                        color:#191a24;
                        font-size:15px;
                        line-height:22px;
                        font-weight:600;
                        text-decoration:none;
                    "
                >
                    {notice["title"]}
                </a>
            </td>
        </tr>
    </table>
    """


def _build_html(notices: list[dict], unsubscribe_url: str) -> str:
    rows = "".join(_render_notice_row(notice) for notice in notices)

    heading = "New Notice" if len(notices) == 1 else f"{len(notices)} New Notices"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Notices</title>
    </head>

    <body
        style="
            margin:0;
            padding:0;
            background:#eef0f6;
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                'Segoe UI',
                Roboto,
                Helvetica,
                Arial,
                sans-serif;
        "
    >

        <!-- OUTER CONTAINER -->
        <table
            role="presentation"
            width="100%"
            cellpadding="0"
            cellspacing="0"
            border="0"
        >
            <tr>
                <td
                    align="center"
                    style="padding:48px 16px;"
                >

                    <!-- EMAIL CARD -->
                    <table
                        role="presentation"
                        width="100%"
                        cellpadding="0"
                        cellspacing="0"
                        border="0"
                        style="
                            max-width:580px;
                            background:#ffffff;
                            border-radius:18px;
                            overflow:hidden;
                        "
                    >

                        <!-- HEADER -->
                        <tr>
                            <td
                                style="
                                    padding:30px 32px 34px;
                                    background:#141e30;
                                    background:linear-gradient(
                                        36deg,
                                        #141e30 0%,
                                        #000000 100%
                                    );
                                    box-shadow: 5px 5px 40px 5px #8f8f8f;
                                "
                            >

                                <!-- BRAND -->
                                <table
                                    role="presentation"
                                    cellpadding="0"
                                    cellspacing="0"
                                    border="0"
                                >
                                    <tr>
                                        <td style="padding-right:9px;">
                                            <div
                                                style="
                                                    width:8px;
                                                    height:8px;
                                                    border-radius:50%;
                                                    background:#8df5c4;
                                                "
                                            ></div>
                                        </td>

                                        <td
                                            style="
                                                color:#b7b3d8;
                                                font-size:11px;
                                                font-weight:600;
                                                letter-spacing:0.12em;
                                            "
                                        >
                                            TU NOTICE
                                        </td>

                                        <td
                                            style="
                                                padding-left:8px;
                                                color:#65617f;
                                                font-size:11px;
                                            "
                                        >
                                            /
                                        </td>

                                        <td
                                            style="
                                                padding-left:8px;
                                                color:#77738f;
                                                font-size:11px;
                                            "
                                        >
                                            IOST
                                        </td>
                                    </tr>
                                </table>


                                <!-- HEADING -->
                                <div
                                    style="
                                        margin-top:38px;
                                        color:#ffffff;
                                        font-size:32px;
                                        line-height:1.15;
                                        font-weight:650;
                                        letter-spacing:-0.8px;
                                    "
                                >
                                    {heading}
                                </div>

                            </td>
                        </tr>


                        <!-- NOTICES -->
                        <tr>
                            <td style="padding:0px 32px 20px;">
                                {rows}
                            </td>
                        </tr>


                        <!-- VIEW ALL -->
                        <tr>
                            <td style="padding:18px 32px 30px;">
                                <a
                                    href="{SITE_URL}"
                                    style="
                                        display:inline-block;
                                        color:#6352c7;
                                        font-size:12px;
                                        font-weight:600;
                                        text-decoration:none;
                                    "
                                >
                                    View all notices&nbsp; →
                                </a>
                            </td>
                        </tr>


                        <!-- FOOTER -->
                        <tr>
                            <td
                                style="
                                    padding:20px 32px 26px;
                                    background:#fafafd;
                                    border-top:1px solid #eeeef3;
                                "
                            >

                                <div
                                    style="
                                        color:#9a9ca7;
                                        font-size:10px;
                                        line-height:17px;
                                    "
                                >
                                    You're receiving this because you
                                    subscribed to <a href="{SITE_URL}" style="color:#9a9ca7; font-size:10px; text-decoration:underline;">notice updates.</a>
                                </div>

                                <div style="margin-top:7px;">
                                    <a
                                        href="{unsubscribe_url}"
                                        style="
                                            color:#747681;
                                            font-size:10px;
                                            text-decoration:underline;
                                        "
                                    >
                                        Unsubscribe
                                    </a>
                                </div>

                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """


async def send_notices_email(
    to_email: str, notices: list[dict], unsubscribe_token: str
) -> dict:
    if not notices:
        return {}

    unsubscribe_url = f"{SITE_URL}/unsubscribe?token={unsubscribe_token}"
    subject = (
        f"New IOST notice: {notices[0]['title']}"
        if len(notices) == 1
        else f"{len(notices)} new IOST notices"
    )

    html_content = _build_html(notices, unsubscribe_url)

    message = EmailMessage()
    message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject

    message["List-Unsubscribe"] = f"<{unsubscribe_url}>"
    message["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

    message.set_content("Your email client doesn't support HTML emails")
    message.add_alternative(html_content, subtype="html")

    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True)
    try:
        await smtp.connect()
        await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)

        await smtp.send_message(message)
    except ConnectionRefusedError:
        logger.exception("Failed to connect to Gmail SMTP: ")
    finally:
        await smtp.quit()

    return {"status": "sent", "to": to_email}
