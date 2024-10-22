"""SMTP Email Helpers"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from operator import itemgetter
from typing import Any


port = 465  # For SSL
password = os.environ.get("SMTP_PWRD", "")
sender_email = os.environ.get("SMTP_EMAIL", "")


test_order = {
    "zip": "30318",
    "country": "US",
    "address2": None,
    "city": "Atlanta",
    "address1": "1040 Huff NW Rd #3211",
    "last_name": "Howard",
    "created_at": 1729481051,
    "total": 120,
    "shipped": 0,
    "tracking_no": None,
    "phone": "3134459333",
    "_id": "1FC1DBFE-9549-4F14-8CFD-30A96A96C2A0",
    "first_name": "Jalin",
    "email": "jhowar39@emich.edu",
    "level_1": "GA",
}

line_item_arg = {
    "item_name": "Cashews",
    "item_variation": "Salted",
    "subtotal": 80,
    "qty": 2,
}


def line_item_html(line_item: dict[str, Any]) -> str:
    """Create Line Item HTML"""
    (item_name, item_variation, subtotal, qty) = itemgetter(
        "item_name", "item_variation", "subtotal", "qty"
    )(line_item)

    name = item_name
    if item_variation:
        name = name + f": {item_variation}"

    return f"""\
            <tr>
                      <td class="pc-w620-halign-left pc-w620-valign-middle pc-w620-width-100pc" align="left" valign="middle" style="padding: 20px 0px 20px 20px; border-bottom: 1px solid #d1dfe3;">
                       <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                        <tr>
                         <td class="pc-w620-align-left" align="left" valign="top" style="padding: 0px 0px 2px 0px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-left" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                           <tr>
                            <td valign="top" class="pc-w620-align-left" align="left" style="padding: 0px 0px 0px 0px;">
                             <div class="pc-font-alt pc-w620-align-left pc-w620-fontSize-14px pc-w620-lineHeight-24" style="line-height: 24px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                              <div><span>{name}</span>
                              </div>
                             </div>
                            </td>
                           </tr>
                          </table>
                         </td>
                        </tr>
                       </table>
                       <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-left" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                        <tr>
                         <td valign="top" class="pc-w620-align-left" align="left">
                          <div class="pc-font-alt pc-w620-align-left" style="line-height: 24px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                           <div><span>Quantity: {qty}</span>
                           </div>
                          </div>
                         </td>
                        </tr>
                       </table>
                      </td>
                      <td class="pc-w620-halign-right pc-w620-valign-bottom pc-w620-width-100pc" align="right" valign="bottom" style="padding: 0px 20px 20px 0px; border-bottom: 1px solid #d1dfe3;">
                       <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                        <tr>
                         <td class="pc-w620-spacing-0-0-0-0 pc-w620-align-right" align="right" valign="top">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-right" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                           <tr>
                            <td valign="top" class="pc-w620-padding-0-0-0-0 pc-w620-align-right" align="right">
                             <div class="pc-font-alt pc-w620-align-right pc-w620-fontSize-14px pc-w620-lineHeight-22" style="line-height: 22px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 800; font-variant-ligatures: normal; color: #121212; text-align: right; text-align-last: right;">
                              <div><span>${subtotal}</span>
                              </div>
                             </div>
                            </td>
                           </tr>
                          </table>
                         </td>
                        </tr>
                       </table>
                      </td>
                     </tr>
"""


def create_order_confirmation(
    _line_items: list[dict[str, Any]],
    order: dict[str, Any],
) -> str:
    """Create order confirmation html"""
    # Format Line Item Rows
    line_items = ""
    quantity = 0
    # for line in _line_items:
    for line in _line_items:
        quantity += line["qty"]
        line_items += line_item_html(line)

    total_items = ""
    if quantity > 1:
        total_items = f"{quantity} items"
    else:
        total_items = f"{quantity} item"

    # Format Shipping Address
    (
        first_name,
        last_name,
        address1,
        address2,
        city,
        level_1,
        _zip,
        total,
    ) = itemgetter(
        "first_name",
        "last_name",
        "address1",
        "address2",
        "city",
        "level_1",
        "zip",
        "total",
    )(
        order
    )

    customer = first_name + f" {last_name}"

    address = address1
    if address2:
        address = address + f" {address2}"

    locality = f"{city}, {level_1} {_zip}"

    return f"""\
<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
 <meta charset="UTF-8" />
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <!--[if !mso]><!-- -->
 <meta http-equiv="X-UA-Compatible" content="IE=edge" />
 <!--<![endif]-->
 <meta name="viewport" content="width=device-width, initial-scale=1.0" />
 <meta name="format-detection" content="telephone=no" />
 <meta name="format-detection" content="date=no" />
 <meta name="format-detection" content="address=no" />
 <meta name="format-detection" content="email=no" />
 <meta name="x-apple-disable-message-reformatting" />
 <link href="https://fonts.googleapis.com/css?family=Nunito+Sans:ital,wght@0,400;0,400;0,600;0,700;0,800" rel="stylesheet" />
 <link href="https://fonts.googleapis.com/css?family=Nunito:ital,wght@0,700" rel="stylesheet" />
 <title>Untitled</title>
 <style>
 html,
         body {{
             margin: 0 !important;
             padding: 0 !important;
             min-height: 100% !important;
             width: 100% !important;
             -webkit-font-smoothing: antialiased;
         }}

         * {{
             -ms-text-size-adjust: 100%;
         }}

         #outlook a {{
             padding: 0;
         }}

         .ReadMsgBody,
         .ExternalClass {{
             width: 100%;
         }}

         .ExternalClass,
         .ExternalClass p,
         .ExternalClass td,
         .ExternalClass div,
         .ExternalClass span,
         .ExternalClass font {{
             line-height: 100%;
         }}

         table,
         td,
         th {{
             mso-table-lspace: 0 !important;
             mso-table-rspace: 0 !important;
             border-collapse: collapse;
         }}

         u + .body table, u + .body td, u + .body th {{
             will-change: transform;
         }}

         body, td, th, p, div, li, a, span {{
             -webkit-text-size-adjust: 100%;
             -ms-text-size-adjust: 100%;
             mso-line-height-rule: exactly;
         }}

         img {{
             border: 0;
             outline: 0;
             line-height: 100%;
             text-decoration: none;
             -ms-interpolation-mode: bicubic;
         }}

         a[x-apple-data-detectors] {{
             color: inherit !important;
             text-decoration: none !important;
         }}

         .pc-gmail-fix {{
             display: none;
             display: none !important;
         }}

         .body .pc-project-body {{
             background-color: transparent !important;
         }}

         @media (min-width: 621px) {{
             .pc-lg-hide {{
                 display: none;
             }}
             .pc-lg-bg-img-hide {{
                 background-image: none !important;
             }}
         }}
 </style>
 <style>
 @media (max-width: 620px) {{
 .pc-project-body {{min-width: 0px !important;}}
 .pc-project-container {{width: 100% !important;}}
 .pc-sm-hide {{display: none !important;}}
 .pc-sm-bg-img-hide {{background-image: none !important;}}
 .pc-w620-padding-20-0-20-0 {{padding: 20px 0px 20px 0px !important;}}
 .pc-w620-itemsSpacings-0-8 {{padding-left: 0px !important;padding-right: 0px !important;padding-top: 4px !important;padding-bottom: 4px !important;}}
 .pc-w620-valign-middle {{vertical-align: middle !important;}}
 td.pc-w620-halign-center,th.pc-w620-halign-center {{text-align: center !important;}}
 table.pc-w620-halign-center {{float: none !important;margin-right: auto !important;margin-left: auto !important;}}
 img.pc-w620-halign-center {{margin-right: auto !important;margin-left: auto !important;}}
 .pc-w620-width-fill {{width: 100% !important;}}
 .pc-w620-padding-20-30-0-30 {{padding: 20px 30px 0px 30px !important;}}
 table.pc-w620-spacing-0-0-0-0 {{margin: 0px 0px 0px 0px !important;}}
 td.pc-w620-spacing-0-0-0-0,th.pc-w620-spacing-0-0-0-0{{margin: 0 !important;padding: 0px 0px 0px 0px !important;}}
 .pc-w620-itemsSpacings-0-30 {{padding-left: 0px !important;padding-right: 0px !important;padding-top: 15px !important;padding-bottom: 15px !important;}}
 .pc-w620-padding-32-20-40-20 {{padding: 32px 20px 40px 20px !important;}}
 .pc-w620-fontSize-36px {{font-size: 36px !important;}}
 .pc-w620-lineHeight-100pc {{line-height: 100% !important;}}
 table.pc-w620-spacing-0-0-12-0 {{margin: 0px 0px 12px 0px !important;}}
 td.pc-w620-spacing-0-0-12-0,th.pc-w620-spacing-0-0-12-0{{margin: 0 !important;padding: 0px 0px 12px 0px !important;}}
 .pc-w620-padding-0-0-0-0 {{padding: 0px 0px 0px 0px !important;}}
 .pc-w620-fontSize-14px {{font-size: 14px !important;}}
 table.pc-w620-spacing-0-0-24-0 {{margin: 0px 0px 24px 0px !important;}}
 td.pc-w620-spacing-0-0-24-0,th.pc-w620-spacing-0-0-24-0{{margin: 0 !important;padding: 0px 0px 24px 0px !important;}}
 .pc-w620-itemsSpacings-0-0 {{padding-left: 0px !important;padding-right: 0px !important;padding-top: 0px !important;padding-bottom: 0px !important;}}

 .pc-w620-width-hug {{width: auto !important;}}
 table.pc-w620-spacing-0-32-12-32 {{margin: 0px 32px 12px 32px !important;}}
 td.pc-w620-spacing-0-32-12-32,th.pc-w620-spacing-0-32-12-32{{margin: 0 !important;padding: 0px 32px 12px 32px !important;}}
 .pc-w620-width-32 {{width: 32px !important;}}
 .pc-w620-height-auto {{height: auto !important;}}
 .pc-w620-width-64 {{width: 64px !important;}}
 .pc-w620-height-1 {{height: 1px !important;}}
 .pc-w620-valign-top {{vertical-align: top !important;}}
 .pc-w620-width-80 {{width: 80px !important;}}
 div.pc-w620-align-center,th.pc-w620-align-center,a.pc-w620-align-center,td.pc-w620-align-center {{text-align: center !important;text-align-last: center !important;}}
 table.pc-w620-align-center {{float: none !important;margin-right: auto !important;margin-left: auto !important;}}
 img.pc-w620-align-center {{margin-right: auto !important;margin-left: auto !important;}}
 .pc-w620-padding-20-24-0-24 {{padding: 20px 24px 0px 24px !important;}}
 .pc-w620-fontSize-32px {{font-size: 32px !important;}}
 .pc-w620-lineHeight-40 {{line-height: 40px !important;}}
 table.pc-w620-spacing-0-0-4-0 {{margin: 0px 0px 4px 0px !important;}}
 td.pc-w620-spacing-0-0-4-0,th.pc-w620-spacing-0-0-4-0{{margin: 0 !important;padding: 0px 0px 4px 0px !important;}}
 .pc-w620-fontSize-16px {{font-size: 16px !important;}}
 .pc-w620-lineHeight-120pc {{line-height: 120% !important;}}
 td.pc-w620-halign-left,th.pc-w620-halign-left {{text-align: left !important;}}
 table.pc-w620-halign-left {{float: none !important;margin-right: auto !important;margin-left: 0 !important;}}
 img.pc-w620-halign-left {{margin-right: auto !important;margin-left: 0 !important;}}
 .pc-w620-padding-20-0-20-20 {{padding: 20px 0px 20px 20px !important;}}
 .pc-w620-width-100pc {{width: 100% !important;}}
 .pc-w620-lineHeight-24 {{line-height: 24px !important;}}
 div.pc-w620-align-left,th.pc-w620-align-left,a.pc-w620-align-left,td.pc-w620-align-left {{text-align: left !important;text-align-last: left !important;}}
 table.pc-w620-align-left{{float: none !important;margin-right: auto !important;margin-left: 0 !important;}}
 img.pc-w620-align-left{{margin-right: auto !important;margin-left: 0 !important;}}
 .pc-w620-valign-bottom {{vertical-align: bottom !important;}}
 td.pc-w620-halign-right,th.pc-w620-halign-right {{text-align: right !important;}}
 table.pc-w620-halign-right {{float: none !important;margin-right: 0 !important;margin-left: auto !important;}}
 img.pc-w620-halign-right {{margin-right: 0 !important;margin-left: auto !important;}}
 .pc-w620-padding-20-20-20-0 {{padding: 20px 20px 20px 0px !important;}}
 .pc-w620-lineHeight-22 {{line-height: 22px !important;}}
 div.pc-w620-align-right,th.pc-w620-align-right,a.pc-w620-align-right,td.pc-w620-align-right {{text-align: right !important;text-align-last: right !important;}}
 table.pc-w620-align-right{{float: none !important;margin-left: auto !important;margin-right: 0 !important;}}
 img.pc-w620-align-right{{margin-right: 0 !important;margin-left: auto !important;}}
 .pc-w620-fontSize-16 {{font-size: 16px !important;}}
 .pc-w620-lineHeight-26 {{line-height: 26px !important;}}
 table.pc-w620-spacing-0-0-8-0 {{margin: 0px 0px 8px 0px !important;}}
 td.pc-w620-spacing-0-0-8-0,th.pc-w620-spacing-0-0-8-0{{margin: 0 !important;padding: 0px 0px 8px 0px !important;}}
 table.pc-w620-spacing-174-0-0-40 {{margin: 174px 0px 0px 40px !important;}}
 td.pc-w620-spacing-174-0-0-40,th.pc-w620-spacing-174-0-0-40{{margin: 0 !important;padding: 174px 0px 0px 40px !important;}}
 .pc-w620-lineHeight-20 {{line-height: 20px !important;}}
 .pc-w620-padding-40-24-0-24 {{padding: 40px 24px 0px 24px !important;}}
 .pc-w620-itemsSpacings-10-20 {{padding-left: 5px !important;padding-right: 5px !important;padding-top: 10px !important;padding-bottom: 10px !important;}}
 .pc-w620-itemsSpacings-0-20 {{padding-left: 0px !important;padding-right: 0px !important;padding-top: 10px !important;padding-bottom: 10px !important;}}
 .pc-w620-fontSize-20px {{font-size: 20px !important;}}
 .pc-w620-padding-32-24-32-24 {{padding: 32px 24px 32px 24px !important;}}
 .pc-w620-itemsSpacings-20-0 {{padding-left: 10px !important;padding-right: 10px !important;padding-top: 0px !important;padding-bottom: 0px !important;}}
 table.pc-w620-spacing-0-0-20-0 {{margin: 0px 0px 20px 0px !important;}}
 td.pc-w620-spacing-0-0-20-0,th.pc-w620-spacing-0-0-20-0{{margin: 0 !important;padding: 0px 0px 20px 0px !important;}}
 .pc-w620-padding-30-24-40-24 {{padding: 30px 24px 40px 24px !important;}}

 .pc-w620-gridCollapsed-1 > tbody,.pc-w620-gridCollapsed-1 > tbody > tr,.pc-w620-gridCollapsed-1 > tr {{display: inline-block !important;}}
 .pc-w620-gridCollapsed-1.pc-width-fill > tbody,.pc-w620-gridCollapsed-1.pc-width-fill > tbody > tr,.pc-w620-gridCollapsed-1.pc-width-fill > tr {{width: 100% !important;}}
 .pc-w620-gridCollapsed-1.pc-w620-width-fill > tbody,.pc-w620-gridCollapsed-1.pc-w620-width-fill > tbody > tr,.pc-w620-gridCollapsed-1.pc-w620-width-fill > tr {{width: 100% !important;}}
 .pc-w620-gridCollapsed-1 > tbody > tr > td,.pc-w620-gridCollapsed-1 > tr > td {{display: block !important;width: auto !important;padding-left: 0 !important;padding-right: 0 !important;margin-left: 0 !important;}}
 .pc-w620-gridCollapsed-1.pc-width-fill > tbody > tr > td,.pc-w620-gridCollapsed-1.pc-width-fill > tr > td {{width: 100% !important;}}
 .pc-w620-gridCollapsed-1.pc-w620-width-fill > tbody > tr > td,.pc-w620-gridCollapsed-1.pc-w620-width-fill > tr > td {{width: 100% !important;}}
 .pc-w620-gridCollapsed-1 > tbody > .pc-grid-tr-first > .pc-grid-td-first,pc-w620-gridCollapsed-1 > .pc-grid-tr-first > .pc-grid-td-first {{padding-top: 0 !important;}}
 .pc-w620-gridCollapsed-1 > tbody > .pc-grid-tr-last > .pc-grid-td-last,pc-w620-gridCollapsed-1 > .pc-grid-tr-last > .pc-grid-td-last {{padding-bottom: 0 !important;}}

 .pc-w620-gridCollapsed-0 > tbody > .pc-grid-tr-first > td,.pc-w620-gridCollapsed-0 > .pc-grid-tr-first > td {{padding-top: 0 !important;}}
 .pc-w620-gridCollapsed-0 > tbody > .pc-grid-tr-last > td,.pc-w620-gridCollapsed-0 > .pc-grid-tr-last > td {{padding-bottom: 0 !important;}}
 .pc-w620-gridCollapsed-0 > tbody > tr > .pc-grid-td-first,.pc-w620-gridCollapsed-0 > tr > .pc-grid-td-first {{padding-left: 0 !important;}}
 .pc-w620-gridCollapsed-0 > tbody > tr > .pc-grid-td-last,.pc-w620-gridCollapsed-0 > tr > .pc-grid-td-last {{padding-right: 0 !important;}}

 .pc-w620-tableCollapsed-1 > tbody,.pc-w620-tableCollapsed-1 > tbody > tr,.pc-w620-tableCollapsed-1 > tr {{display: block !important;}}
 .pc-w620-tableCollapsed-1.pc-width-fill > tbody,.pc-w620-tableCollapsed-1.pc-width-fill > tbody > tr,.pc-w620-tableCollapsed-1.pc-width-fill > tr {{width: 100% !important;}}
 .pc-w620-tableCollapsed-1.pc-w620-width-fill > tbody,.pc-w620-tableCollapsed-1.pc-w620-width-fill > tbody > tr,.pc-w620-tableCollapsed-1.pc-w620-width-fill > tr {{width: 100% !important;}}
 .pc-w620-tableCollapsed-1 > tbody > tr > td,.pc-w620-tableCollapsed-1 > tr > td {{display: block !important;width: auto !important;}}
 .pc-w620-tableCollapsed-1.pc-width-fill > tbody > tr > td,.pc-w620-tableCollapsed-1.pc-width-fill > tr > td {{width: 100% !important;box-sizing: border-box !important;}}
 .pc-w620-tableCollapsed-1.pc-w620-width-fill > tbody > tr > td,.pc-w620-tableCollapsed-1.pc-w620-width-fill > tr > td {{width: 100% !important;box-sizing: border-box !important;}}
 }}
 </style>
 <!--[if !mso]><!-- -->
 <style>
 @media all {{ @font-face {{ font-family: 'Nunito Sans'; font-style: normal; font-weight: 600; src: url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GCC5XvVUj.woff') format('woff'), url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GCC5XvVUl.woff2') format('woff2'); }} @font-face {{ font-family: 'Nunito Sans'; font-style: normal; font-weight: 700; src: url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GMS5XvVUj.woff') format('woff'), url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GMS5XvVUl.woff2') format('woff2'); }} @font-face {{ font-family: 'Nunito Sans'; font-style: normal; font-weight: 400; src: url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4G1ilXvVUj.woff') format('woff'), url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4G1ilXvVUl.woff2') format('woff2'); }} @font-face {{ font-family: 'Nunito Sans'; font-style: normal; font-weight: 800; src: url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GVi5XvVUj.woff') format('woff'), url('https://fonts.gstatic.com/s/nunitosans/v15/pe1mMImSLYBIv1o4X1M8ce2xCx3yop4tQpF_MeTm0lfGWVpNn64CL7U8upHZIbMV51Q42ptCp5F5bxqqtQ1yiU4GVi5XvVUl.woff2') format('woff2'); }} @font-face {{ font-family: 'Nunito'; font-style: normal; font-weight: 700; src: url('https://fonts.gstatic.com/s/nunito/v26/XRXI3I6Li01BKofiOc5wtlZ2di8HDFwmdTo3iQ.woff') format('woff'), url('https://fonts.gstatic.com/s/nunito/v26/XRXI3I6Li01BKofiOc5wtlZ2di8HDFwmdTo3jw.woff2') format('woff2'); }} }}
 </style>
 <!--<![endif]-->
 <!--[if mso]>
    <style type="text/css">
        .pc-font-alt {{
            font-family: Arial, Helvetica, sans-serif !important;
        }}
    </style>
    <![endif]-->
 <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
</head>

<body class="body pc-font-alt" style="width: 100% !important; min-height: 100% !important; margin: 0 !important; padding: 0 !important; line-height: 1.5; color: #2D3A41; mso-line-height-rule: exactly; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-variant-ligatures: normal; text-rendering: optimizeLegibility; -moz-osx-font-smoothing: grayscale; background-color: #ffefcf;" bgcolor="#ffefcf">
 <table class="pc-project-body" style="table-layout: fixed; min-width: 600px; background-color: #ffefcf;" bgcolor="#ffefcf" width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
  <tr>
   <td align="center" valign="top">
    <table class="pc-project-container" align="center" width="600" style="width: 600px; max-width: 600px;" border="0" cellpadding="0" cellspacing="0" role="presentation">
     <tr>
      <td class="pc-w620-padding-20-0-20-0" style="padding: 20px 0px 20px 0px;" align="left" valign="top">
       <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="width: 100%;">
        <tr>
         <td valign="top">
          <!-- BEGIN MODULE: Menu -->
          <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
           <tr>
            <td class="pc-w620-spacing-0-0-0-0" style="padding: 0px 0px 0px 0px;">
             <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
              <tr>
               <td valign="top" class="pc-w620-padding-20-30-0-30" style="padding: 26px 32px 16px 32px; border-radius: 0px; background-color: #c4003f;" bgcolor="#c4003f">
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td class="pc-w620-valign-middle pc-w620-halign-center">
                   <table class="pc-width-fill pc-w620-gridCollapsed-1 pc-w620-halign-center" width="100%" height="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                    <tr class="pc-grid-tr-first pc-grid-tr-last">
                     <td class="pc-grid-td-first pc-w620-itemsSpacings-0-8" align="left" valign="top" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                      <table class="pc-w620-width-fill pc-w620-halign-center" style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                       <tr>
                        <td class="pc-w620-halign-center pc-w620-valign-middle" align="left" valign="top">
                         <table class="pc-w620-halign-center" align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                          <tr>
                           <td class="pc-w620-halign-center" align="left" valign="top">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td class="pc-w620-halign-center" align="left" valign="top">
                               <img src="https://cloudfilesdm.com/postcards/1e5e9dcb8949cdb497783fd116d022f2.png" class="pc-w620-halign-center" width="134" height="77" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; object-fit: contain; width:134px; height: auto; max-width: 100%; border: 0;" />
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                         </table>
                        </td>
                       </tr>
                      </table>
                     </td>
                     <td class="pc-grid-td-last pc-w620-itemsSpacings-0-8" align="left" valign="top" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                      <table class="pc-w620-halign-center" style="border-collapse: separate; border-spacing: 0; height: 100%;" height="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                       <tr>
                        <td align="right" valign="bottom">
                         <table align="right" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                          <tr>
                           <td align="right" valign="top">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td align="right" valign="top">
                               <img src="https://cloudfilesdm.com/postcards/64a25f93e3b6037c51a72aa2c61148a1.png" class="" width="67" height="59" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; object-fit: contain; width:67px; height: auto; max-width: 100%; border: 0;" />
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                         </table>
                        </td>
                       </tr>
                      </table>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
               </td>
              </tr>
             </table>
            </td>
           </tr>
          </table>
          <!-- END MODULE: Menu -->
         </td>
        </tr>
        <tr>
         <td valign="top">
          <!-- BEGIN MODULE: Order Status -->
          <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
           <tr>
            <td class="pc-w620-spacing-0-0-0-0" style="padding: 0px 0px 0px 0px;">
             <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
              <tr>
               <td valign="top" class="pc-w620-padding-20-24-0-24" style="padding: 0px 32px 0px 32px; border-radius: 0px; background-color: #c4003f;" bgcolor="#c4003f">
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td>
                   <table class="pc-width-fill pc-w620-gridCollapsed-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                    <tr class="pc-grid-tr-first pc-grid-tr-last">
                     <td class="pc-grid-td-first pc-grid-td-last pc-w620-itemsSpacings-0-30" align="left" valign="top" style="width: 50%; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                      <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                       <tr>
                        <td class="pc-w620-padding-32-20-40-20" align="center" valign="middle" style="padding: 48px 24px 48px 24px; background-color: #fff8f0; border-radius: 12px 12px 12px 12px;">
                         <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                          <tr>
                           <td align="center" valign="top">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td class="pc-w620-spacing-0-0-12-0" valign="top" style="padding: 0px 0px 12px 0px;">
                               <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0;">
                                <tr>
                                 <td valign="top" class="pc-w620-padding-0-0-0-0" align="center" style="padding: 0px 0px 0px 0px;">
                                  <div class="pc-font-alt pc-w620-fontSize-36px pc-w620-lineHeight-100pc" style="line-height: 110%; letter-spacing: -1px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 44px; font-weight: bold; font-variant-ligatures: normal; color: #121212; text-align: center; text-align-last: center;">
                                   <div><span>Your order has been confirmed.</span>
                                   </div>
                                  </div>
                                 </td>
                                </tr>
                               </table>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                          <tr>
                           <td align="center" valign="top">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td class="pc-w620-spacing-0-0-24-0" valign="top" style="padding: 0px 0px 24px 0px;">
                               <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0;">
                                <tr>
                                 <td valign="top" class="pc-w620-padding-0-0-0-0" align="center" style="padding: 0px 0px 0px 0px;">
                                  <div class="pc-font-alt pc-w620-fontSize-14px" style="line-height: 150%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #121212cc; text-align: center; text-align-last: center;">
                                   <div><span style="font-weight: 400;font-style: normal;">My Left Nuts</span><span style="font-weight: 400;font-style: normal;color: rgb(31, 31, 31);">® </span><span style="font-weight: 400;font-style: normal;">will commence work on this immediately. You&#39;ll receive an email notification once it&#39;s shipped.</span>
                                   </div>
                                  </div>
                                 </td>
                                </tr>
                               </table>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                          <tr>
                           <td align="center" valign="top">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td class="pc-w620-spacing-0-32-12-32 pc-w620-valign-middle pc-w620-halign-center" align="center" style="padding: 0px 0px 12px 0px;">
                               <table class="pc-width-hug pc-w620-gridCollapsed-0 pc-w620-width-hug pc-w620-halign-center" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                <tr class="pc-grid-tr-first pc-grid-tr-last">
                                 <td class="pc-grid-td-first pc-w620-itemsSpacings-0-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td class="pc-w620-halign-center pc-w620-valign-middle" align="center" valign="middle">
                                     <table class="pc-w620-halign-center" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td class="pc-w620-halign-center" align="center" valign="top">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td class="pc-w620-halign-center" align="center" valign="top" style="padding: 0px 0px 0px 0px;">
                                           <img src="https://cloudfilesdm.com/postcards/image-1702452390921.png" class="pc-w620-width-32 pc-w620-height-auto pc-w620-halign-center" width="40" height="40" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width:40px; height: auto; max-width: 100%; border: 0;" />
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-w620-itemsSpacings-0-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td class="pc-w620-halign-center pc-w620-valign-middle" align="left" valign="middle">
                                     <table class="pc-w620-halign-center" align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td class="pc-w620-halign-center" align="left" valign="top">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                         <tr>
                                          <td valign="top">
                                           <table class="pc-w620-width-64  pc-w620-halign-center" width="124" border="0" cellpadding="0" cellspacing="0" role="presentation" style="margin-right: auto;">
                                            <tr>
                                             <!--[if gte mso 9]>
                    <td height="1" valign="top" style="line-height: 1px; font-size: 1px; border-bottom: 1px solid #000000;">&nbsp;</td>
                <![endif]-->
                                             <!--[if !gte mso 9]><!-- -->
                                             <td height="1" valign="top" style="line-height: 1px; font-size: 1px; border-bottom: 1px solid #000000;">&nbsp;</td>
                                             <!--<![endif]-->
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-w620-itemsSpacings-0-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td align="center" valign="middle">
                                     <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td align="center" valign="top">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td align="center" valign="top" style="padding: 0px 0px 0px 0px;">
                                           <img src="https://cloudfilesdm.com/postcards/image-1702463224472.png" class="pc-w620-width-32 pc-w620-height-auto" width="40" height="40" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width:40px; height: auto; max-width: 100%; border: 0;" />
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-w620-itemsSpacings-0-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td class="pc-w620-halign-center pc-w620-valign-middle" align="left" valign="top">
                                     <table class="pc-w620-halign-center" align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td class="pc-w620-halign-center" align="left" valign="top">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                         <tr>
                                          <td valign="top">
                                           <table class="pc-w620-width-64  pc-w620-halign-center" width="124" border="0" cellpadding="0" cellspacing="0" role="presentation" style="margin-right: auto;">
                                            <tr>
                                             <!--[if gte mso 9]>
                    <td height="1" valign="top" style="line-height: 1px; font-size: 1px; border-bottom: 1px solid #000000;">&nbsp;</td>
                <![endif]-->
                                             <!--[if !gte mso 9]><!-- -->
                                             <td height="1" valign="top" style="line-height: 1px; font-size: 1px; border-bottom: 1px solid #000000;">&nbsp;</td>
                                             <!--<![endif]-->
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-grid-td-last pc-w620-itemsSpacings-0-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td class="pc-w620-halign-center pc-w620-valign-middle" align="center" valign="middle">
                                     <table class="pc-w620-halign-center" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td class="pc-w620-halign-center" align="center" valign="top">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td class="pc-w620-halign-center" align="center" valign="top" style="padding: 0px 0px 0px 0px;">
                                           <img src="https://cloudfilesdm.com/postcards/image-1702463242847.png" class="pc-w620-width-32 pc-w620-height-auto pc-w620-halign-center" width="40" height="40" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width:40px; height: auto; max-width: 100%; border: 0;" />
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                </tr>
                               </table>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                          <tr>
                           <td align="center" valign="top">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td class="pc-w620-spacing-0-0-24-0 pc-w620-valign-top pc-w620-halign-center" style="padding: 0px 0px 24px 0px;">
                               <table class="pc-width-fill pc-w620-gridCollapsed-0 pc-w620-width-fill pc-w620-halign-center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                <tr class="pc-grid-tr-first pc-grid-tr-last">
                                 <td class="pc-grid-td-first pc-w620-itemsSpacings-0-0" align="center" valign="top" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill pc-w620-halign-center" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td align="center" valign="middle">
                                     <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td align="center" valign="top">
                                        <table class="pc-w620-width-80" width="80" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td valign="top" style="padding: 0px 0px 0px 0px;">
                                           <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="center" style="border-collapse: separate; border-spacing: 0;">
                                            <tr>
                                             <td valign="top" class="pc-w620-align-center" align="center" style="padding: 0px 0px 0px 0px;">
                                              <div class="pc-font-alt pc-w620-align-center pc-w620-fontSize-14px" style="line-height: 120%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #121212cc; text-align: center; text-align-last: center;">
                                               <div><span style="font-weight: 400;font-style: normal;">Order Confirmed</span>
                                               </div>
                                              </div>
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-w620-itemsSpacings-0-0" align="center" valign="top" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill pc-w620-halign-center" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td align="center" valign="middle">
                                     <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td align="center" valign="top">
                                        <table class="pc-w620-width-80" width="80" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td valign="top" style="padding: 0px 0px 0px 0px;">
                                           <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="center" style="border-collapse: separate; border-spacing: 0;">
                                            <tr>
                                             <td valign="top" align="center" style="padding: 0px 0px 0px 0px;">
                                              <div class="pc-font-alt pc-w620-fontSize-14px" style="line-height: 120%; letter-spacing: 0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #121212cc; text-align: center; text-align-last: center;">
                                               <div><span style="font-weight: 400;font-style: normal;">Shipped</span>
                                               </div>
                                              </div>
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                 <td class="pc-grid-td-last pc-w620-itemsSpacings-0-0" align="center" valign="top" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                  <table class="pc-w620-width-fill pc-w620-halign-center" style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr>
                                    <td align="center" valign="middle">
                                     <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                      <tr>
                                       <td align="center" valign="top">
                                        <table class="pc-w620-width-80" width="80" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                         <tr>
                                          <td valign="top" style="padding: 0px 0px 0px 0px;">
                                           <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="center" style="border-collapse: separate; border-spacing: 0;">
                                            <tr>
                                             <td valign="top" class="pc-w620-align-center" align="center" style="padding: 0px 0px 0px 0px;">
                                              <div class="pc-font-alt pc-w620-align-center pc-w620-fontSize-14px" style="line-height: 120%; letter-spacing: 0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #121212cc; text-align: center; text-align-last: center;">
                                               <div><span style="font-weight: 400;font-style: normal;">Expected</span>
                                               </div>
                                               <div><span style="font-weight: 400;font-style: normal;">Delivered</span>
                                               </div>
                                              </div>
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                </tr>
                               </table>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                         </table>
                        </td>
                       </tr>
                      </table>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
               </td>
              </tr>
             </table>
            </td>
           </tr>
          </table>
          <!-- END MODULE: Order Status -->
         </td>
        </tr>
        <tr>
         <td valign="top">
          <!-- BEGIN MODULE: Order Details -->
          <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
           <tr>
            <td class="pc-w620-spacing-0-0-0-0" style="padding: 0px 0px 0px 0px;">
             <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
              <tr>
               <td valign="top" class="pc-w620-padding-40-24-0-24" style="padding: 48px 32px 0px 32px; border-radius: 0px; background-color: #c4003f;" bgcolor="#c4003f">
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td class="pc-w620-spacing-0-0-4-0" align="center" valign="top" style="padding: 0px 0px 8px 0px;">
                   <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                    <tr>
                     <td valign="top" class="pc-w620-padding-0-0-0-0" align="center" style="padding: 0px 0px 0px 0px;">
                      <div class="pc-font-alt pc-w620-fontSize-32px pc-w620-lineHeight-40" style="line-height: 120%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 32px; font-weight: bold; font-variant-ligatures: normal; color: #ffffff; text-align: center; text-align-last: center;">
                       <div><span style="color: #ffffff;">Order details</span>
                       </div>
                      </div>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td align="center" valign="top" style="padding: 0px 0px 24px 0px;">
                   <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                    <tr>
                     <td valign="top" align="center" style="padding: 0px 0px 0px 0px;">
                      <div class="pc-font-alt pc-w620-fontSize-16px pc-w620-lineHeight-120pc" style="line-height: 150%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: 600; font-variant-ligatures: normal; color: #ffffffcc; text-align: center; text-align-last: center;">
                       <div><span style="color: #ffffffcc;">Confirmation number: {order['_id']}</span>
                       </div>
                      </div>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td style="padding: 0px 0px 0px 0px; ">
                   <table class="pc-w620-width-fill pc-w620-tableCollapsed-0" border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" bgcolor="#FFFFFF" style="border-collapse: separate; border-spacing: 0; width: 100%; background-color:#FFFFFF; border-top: 1px solid #d1dfe3; border-right: 1px solid #d1dfe3; border-bottom: 1px solid #d1dfe3; border-left: 1px solid #d1dfe3; border-radius: 12px 12px 12px 12px; overflow: hidden;">
                    <tbody>
                     <tr>
                      {line_items}
                     <tr>
                      <td class="pc-w620-halign-left pc-w620-valign-middle pc-w620-width-100pc" align="left" valign="top" style="padding: 20px 0px 20px 20px; border-bottom: 1px solid #d1dfe3;">
                       <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                        <tr>
                         <td>
                          <table class="pc-width-fill pc-w620-gridCollapsed-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                           <tr class="pc-grid-tr-first pc-grid-tr-last">
                            <td class="pc-grid-td-first pc-w620-itemsSpacings-0-30" align="left" valign="top" style="width: 50%; padding-top: 0px; padding-right: 20px; padding-bottom: 0px; padding-left: 0px;">
                             <table style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                              <tr>
                               <td align="left" valign="top">
                                <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                 <tr>
                                  <td align="left" valign="top">
                                   <table align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                    <tr>
                                     <td class="pc-w620-spacing-0-0-8-0" valign="top" style="padding: 0px 0px 8px 0px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0;">
                                       <tr>
                                        <td valign="top" class="pc-w620-padding-0-0-0-0 pc-w620-align-left" align="left" style="padding: 0px 0px 0px 0px;">
                                         <div class="pc-font-alt pc-w620-align-left pc-w620-fontSize-16 pc-w620-lineHeight-26" style="line-height: 24px; letter-spacing: 0px; font-family: 'Nunito', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: bold; font-variant-ligatures: normal; color: #121212; text-align: left; text-align-last: left;">
                                          <div><span>Shipping address</span>
                                          </div>
                                         </div>
                                        </td>
                                       </tr>
                                      </table>
                                     </td>
                                    </tr>
                                   </table>
                                  </td>
                                 </tr>
                                 <tr>
                                  <td align="left" valign="top">
                                   <table align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                    <tr>
                                     <td valign="top" style="padding: 0px 0px 2px 0px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0;">
                                       <tr>
                                        <td valign="top" class="pc-w620-align-left" align="left">
                                         <div class="pc-font-alt pc-w620-align-left" style="line-height: 24px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                                          <div><span>{customer}</span>
                                          </div>
                                         </div>
                                        </td>
                                       </tr>
                                      </table>
                                     </td>
                                    </tr>
                                   </table>
                                  </td>
                                 </tr>
                                 <tr>
                                  <td align="left" valign="top">
                                   <table align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                    <tr>
                                     <td valign="top" style="padding: 0px 0px 2px 0px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="border-collapse: separate; border-spacing: 0;">
                                       <tr>
                                        <td valign="top" class="pc-w620-align-left" align="left">
                                         <div class="pc-font-alt pc-w620-align-left" style="line-height: 24px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                                          <div><span>{address}</span>
                                          </div>
                                         </div>
                                        </td>
                                       </tr>
                                      </table>
                                     </td>
                                    </tr>
                                   </table>
                                  </td>
                                 </tr>
                                 <tr>
                                  <td align="left" valign="top">
                                   <table width="100%" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                    <tr>
                                     <td valign="top" style="padding: 0px 0px 2px 0px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="left" style="border-collapse: separate; border-spacing: 0;">
                                       <tr>
                                        <td valign="top" class="pc-w620-align-left" align="left" style="padding: 0px 0px 0px 0px;">
                                         <div class="pc-font-alt pc-w620-align-left" style="line-height: 24px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                                          <div><span>{locality}</span>
                                          </div>
                                         </div>
                                        </td>
                                       </tr>
                                      </table>
                                     </td>
                                    </tr>
                                   </table>
                                  </td>
                                 </tr>
                                 <tr>
                                  <td align="left" valign="top">
                                   <table width="100%" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                    <tr>
                                     <td valign="top">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="left" style="border-collapse: separate; border-spacing: 0;">
                                       <tr>
                                        <td valign="top" class="pc-w620-align-left" align="left">
                                         <div class="pc-font-alt pc-w620-align-left" style="line-height: 20px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 600; font-variant-ligatures: normal; color: #121212cc; text-align: left; text-align-last: left;">
                                          <div><span>United States</span>
                                          </div>
                                         </div>
                                        </td>
                                       </tr>
                                      </table>
                                     </td>
                                    </tr>
                                   </table>
                                  </td>
                                 </tr>
                                </table>
                               </td>
                              </tr>
                             </table>
                            </td>
                           </tr>
                          </table>
                         </td>
                        </tr>
                       </table>
                      </td>

                     </tr>
                     <tr align="left" valign="middle">
                      <td class="pc-w620-halign-left pc-w620-valign-middle pc-w620-width-100pc" align="left" valign="middle" style="padding: 20px 0px 20px 20px;">
                       <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                        <tr>
                         <td class="pc-w620-spacing-0-0-0-0 pc-w620-align-left" align="left" valign="top">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-left" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                           <tr>
                            <td valign="top" class="pc-w620-padding-0-0-0-0 pc-w620-align-left" align="left">
                             <div class="pc-font-alt pc-w620-align-left pc-w620-fontSize-16 pc-w620-lineHeight-20" style="line-height: 22px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: bold; font-variant-ligatures: normal; color: #121212; text-align: left; text-align-last: left;">
                              <div><span>Total ({total_items})</span>
                              </div>
                             </div>
                            </td>
                           </tr>
                          </table>
                         </td>
                        </tr>
                       </table>
                      </td>
                      <td class="pc-w620-halign-right pc-w620-valign-bottom pc-w620-width-100pc" align="right" valign="middle" style="padding: 20px 20px 20px 20px;">
                       <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                        <tr>
                         <td class="pc-w620-spacing-0-0-0-0 pc-w620-align-right" align="right" valign="top">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-right" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                           <tr>
                            <td valign="top" class="pc-w620-padding-0-0-0-0 pc-w620-align-right" align="right">
                             <div class="pc-font-alt pc-w620-align-right pc-w620-fontSize-16px pc-w620-lineHeight-20" style="line-height: 22px; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 20px; font-weight: 800; font-variant-ligatures: normal; color: #121212; text-align: right; text-align-last: right;">
                              <div><span>${total}</span>
                              </div>
                             </div>
                            </td>
                           </tr>
                          </table>
                         </td>
                        </tr>
                       </table>
                      </td>
                     </tr>
                    </tbody>
                   </table>
                  </td>
                 </tr>
                </table>
               </td>
              </tr>
             </table>
            </td>
           </tr>
          </table>
          <!-- END MODULE: Order Details -->
         </td>
        </tr>
        <tr>
         <td valign="top">
          <!-- BEGIN MODULE: Questions? -->
          <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
           <tr>
            <td class="pc-w620-spacing-0-0-0-0" style="padding: 0px 0px 0px 0px;">
             <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
              <tr>
               <td valign="top" class="pc-w620-padding-32-24-32-24" style="padding: 48px 32px 48px 32px; border-radius: 0px; background-color: #c4003f;" bgcolor="#c4003f">
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td align="left">
                   <table align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                    <tr>
                     <td valign="top">
                      <table class="pc-width-hug pc-w620-gridCollapsed-1" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                       <tr class="pc-grid-tr-first pc-grid-tr-last">
                        <td class="pc-grid-td-first pc-grid-td-last pc-w620-itemsSpacings-10-20" valign="top" style="width: 50%; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                         <table style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                          <tr>
                           <td class="pc-w620-halign-center pc-w620-valign-top" align="left" valign="top" style="padding: 20px 20px 20px 20px; background-color: #fff8f0; border-radius: 8px 8px 8px 8px;">
                            <table class="pc-w620-halign-center" align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                             <tr>
                              <td class="pc-w620-halign-center" align="left" valign="top">
                               <table class="pc-w620-halign-center" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                <tr>
                                 <td class="pc-w620-valign-middle pc-w620-halign-center" align="left">
                                  <table class="pc-width-hug pc-w620-gridCollapsed-1 pc-w620-halign-center" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                   <tr class="pc-grid-tr-first pc-grid-tr-last">
                                    <td class="pc-grid-td-first pc-w620-itemsSpacings-0-20" valign="middle" style="padding-top: 0px; padding-right: 6px; padding-bottom: 0px; padding-left: 0px;">
                                     <table class="pc-w620-width-fill" style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                      <tr>
                                       <td class="pc-w620-padding-0-0-0-0 pc-w620-halign-center pc-w620-valign-middle" align="left" valign="middle" style="padding: 0px 11px 0px 2px;">
                                        <table class="pc-w620-halign-center" align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                         <tr>
                                          <td class="pc-w620-halign-center" align="left" valign="top">
                                           <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                            <tr>
                                             <td class="pc-w620-halign-center" align="left" valign="top">
                                              <img src="https://cloudfilesdm.com/postcards/image-1702460591798.png" class="pc-w620-align-center" width="64" height="64" alt="" style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width:64px; height: auto; max-width: 100%; border: 0;" />
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                    <td class="pc-grid-td-last pc-w620-itemsSpacings-0-20" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 6px;">
                                     <table style="border-collapse: separate; border-spacing: 0; width: 100%;" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                      <tr>
                                       <td align="left" valign="middle" style="padding: 0px 0px 0px 0px;">
                                        <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                                         <tr>
                                          <td align="left" valign="top">
                                           <table width="100%" align="left" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                            <tr>
                                             <td valign="top" style="padding: 0px 0px 4px 0px;">
                                              <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" align="left" style="border-collapse: separate; border-spacing: 0;">
                                               <tr>
                                                <td valign="top" class="pc-w620-align-center" align="left" style="padding: 0px 0px 0px 0px;">
                                                 <div class="pc-font-alt pc-w620-align-center pc-w620-fontSize-20px" style="line-height: 21px; letter-spacing: -0.2px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; font-variant-ligatures: normal; color: #121212; text-align: left; text-align-last: left;">
                                                  <div><span style="letter-spacing: 0px;">Any questions?</span>
                                                  </div>
                                                 </div>
                                                </td>
                                               </tr>
                                              </table>
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                         <tr>
                                          <td align="left" valign="top">
                                           <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="left" style="border-collapse: separate; border-spacing: 0;">
                                            <tr>
                                             <td valign="top" class="pc-w620-align-center" align="left">
                                              <div class="pc-font-alt pc-w620-align-center" style="line-height: 140%; letter-spacing: -0.2px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 15px; font-weight: normal; font-variant-ligatures: normal; color: #333333; text-align: left; text-align-last: left;">
                                               <div><span style="color: rgb(18, 18, 18);">﻿If you need any help whatsoever or just want to chat, email us anytime </span><span style="font-weight: 600;font-style: normal;color: rgb(255, 85, 74);">info@myleft.org</span>
                                               </div>
                                              </div>
                                             </td>
                                            </tr>
                                           </table>
                                          </td>
                                         </tr>
                                        </table>
                                       </td>
                                      </tr>
                                     </table>
                                    </td>
                                   </tr>
                                  </table>
                                 </td>
                                </tr>
                               </table>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                         </table>
                        </td>
                       </tr>
                      </table>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
               </td>
              </tr>
             </table>
            </td>
           </tr>
          </table>
          <!-- END MODULE: Questions? -->
         </td>
        </tr>
        <tr>
         <td valign="top">
          <!-- BEGIN MODULE: Footer -->
          <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
           <tr>
            <td class="pc-w620-spacing-0-0-0-0" style="padding: 0px 0px 0px 0px;">
             <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
              <tr>
               <td valign="top" class="pc-w620-padding-30-24-40-24" style="padding: 50px 40px 50px 40px; border-radius: 0px; background-color: #0a3161;" bgcolor="#0a3161">
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td class="pc-w620-spacing-0-0-20-0" align="center" style="padding: 0px 0px 40px 0px;">
                   <table class="pc-width-hug pc-w620-gridCollapsed-0" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                    <tr class="pc-grid-tr-first pc-grid-tr-last">
                     <td class="pc-grid-td-first pc-grid-td-last pc-w620-itemsSpacings-20-0" valign="middle" style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                      <table style="border-collapse: separate; border-spacing: 0;" border="0" cellpadding="0" cellspacing="0" role="presentation">
                       <tr>
                        <td align="center" valign="middle">
                         <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width: 100%;">
                          <tr>
                           <td align="center" valign="top">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation">
                             <tr>
                              <td valign="top">
                                <a href="https://www.x.com/myleftsnuts">
                               <img src="https://cloudfilesdm.com/postcards/2249492905cbf066d1e2999ef53bc950.png" class="" width="20" height="20" style="display: block; border: 0; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width: 20px; height: 20px;" alt="Link to My Left X profile." />
                               </a>
                              </td>
                             </tr>
                            </table>
                           </td>
                          </tr>
                         </table>
                        </td>
                       </tr>
                      </table>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td class="pc-w620-align-center" align="center" valign="top" style="padding: 0px 0px 20px 0px;">
                   <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-center" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                    <tr>
                     <td valign="top" class="pc-w620-align-center" align="center" style="padding: 0px 0px 0px 0px;">
                      <div class="pc-font-alt pc-w620-align-center pc-w620-fontSize-14px" style="line-height: 130%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #ffffffcc; text-align: center; text-align-last: center;">
                       <div><span>© My Left Nuts. All Rights Reserved.</span>
                       </div>
                      </div>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
                <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                 <tr>
                  <td class="pc-w620-spacing-0-0-0-0 pc-w620-align-center" align="center" valign="top" style="padding: 0px 0px 0px 0px;">
                   <table border="0" cellpadding="0" cellspacing="0" role="presentation" class="pc-w620-align-center" width="100%" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                    <tr>
                     <td valign="top" class="pc-w620-padding-0-0-0-0 pc-w620-align-center" align="center" style="padding: 0px 0px 0px 0px;">
                      <div class="pc-font-alt pc-w620-align-center pc-w620-fontSize-14px" style="line-height: 130%; letter-spacing: -0px; font-family: 'Nunito Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: normal; font-variant-ligatures: normal; color: #ffffffcc; text-align: center; text-align-last: center;">
                       <div><span>Prefer not to receive these emails anymore </span><a href="https://www.myleft.org" style="text-decoration: none; color: #ffffffcc;"><span style="text-decoration: underline;font-weight: 600;font-style: normal;color: rgb(255, 255, 255);">Unsubscribe here.</span></a><span>&#xFEFF;</span>
                       </div>
                      </div>
                     </td>
                    </tr>
                   </table>
                  </td>
                 </tr>
                </table>
               </td>
              </tr>
             </table>
            </td>
           </tr>
          </table>
          <!-- END MODULE: Footer -->
         </td>
        </tr>
       </table>
      </td>
     </tr>
    </table>
   </td>
  </tr>
 </table>
 <!-- Fix for Gmail on iOS -->
 <div class="pc-gmail-fix" style="white-space: nowrap; font: 15px courier; line-height: 0;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
 </div>
</body>

</html>
"""


def send_order_email(
    order: dict[str, Any], line_items: list[dict[str, Any]]
) -> None:
    """Send order confirmation email

    Args:
        order (dict[str, Any]): order
        line_items (list[dict[str, Any]]): line items.
    """
    receiver_email = order["email"]
    message = MIMEMultipart("alternative")
    message[
        "Subject"
    ] = f"My Left - Order Confirmation: {order['_id']}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(message["Subject"], "plain")
    part2 = MIMEText(
        create_order_confirmation(line_items, order), "html"
    )

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com") as server:
        server.login(sender_email, password)
        server.ehlo()
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        server.close()
