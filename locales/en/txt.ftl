# -------------------------------------- Registration --------------------------------------

hello-new-user =
    🎉 <b>Hello!</b>

    This bot is part of the group 📡 <b>@QO100RUSSIA 🇷🇺</b>
    Bot developer: <b>Vladimir R3LO</b>

    <b>Using a bot, you can:</b>
    ➡️ Maintaining you QO-100 log in Telegram
    ➡️ QSO search in the uploaded log
    ➡️ Log conversion to different formats
    ➡️ Synchronize your log with LoTW
    ➡️ Download your log in ADIF and CSV format with QO-100 tags
    ➡️ Obtaining electronic diplomas according to the diploma program QO-100=RUSSIA

    💡 To start the bot, you need go through a simple registration. Click on the REGISTER button below 👇

registration-button = Register

nil-cancel = Nothing to cancel.

reg-cancel = Registration cancelled.
    To start new registration, run /start

regist-call =
    ⭐️ <b>Let's start registration</b>

    1️⃣ Enter your primary callsign in the message 👇
    If you want to abort registration run /cancel

regist-name = ⭐️ Your callsign is <b>{ $reg_call }</b>

    2️⃣ Enter your name and surname in the message 👇
    Your name will be write down on your diplomas.
    If you want to abort registration, run /cancel

regist-complit =
    ⭐️ Registration completed successfully! 👍

    <b>Your registration</b>

    ✅ Callsign: <b>{ $reg_call }</b>
    ✅ Name: <b>{ $reg_name }</b>

    ☰ Main menu

# -------------------------------------- Main Menu --------------------------------------

main-menu = ☰ Main menu

upload-log = ↗️ Upload Log

download-log = ↘️ Download Log

convert-log = 🌀 Convert any ADIF log

wipe-log = 🗑 Wipe log

worked-statistics = 📊 My log info

my-awards = 🏆 My Awards

users-raitings = 📈 Users Ranking

# -------------------------------------- Menu Ranking --------------------------------------

ranking-title = 📈 <b>TLog</b> ~ Users ranking 🛰 QO-100

ranking-qthloc = 🗂 QTH locators

ranking-unique = 🔰 Unique callsigns

ranking-dxcc = 🌐 DXCC Counties

ranking-rus = 🇷🇺 Russian regions

ranking-based = <i>[ Based on LoTW report ]</i>

# -------------------------------------- Awards --------------------------------------

awards-title = 🏆 Diploma rules 📡 QO-100-RUSSIA

    ➡️ <b>W-QO100-R</b> - worked with 25 regions of 🇷🇺 Russia
    ➡️ <b>W-QO100-C</b> - worked with 100 countries on the DXCC list
    ➡️ <b>W-QO100-L</b> - worked with 500 different QTH locators
    ➡️ <b>W-QO100-U</b> - worked with 1000 different callsigns
    ➡️ <b>W-QO100-B</b> - basic diploma, 1000 QSOs in the log

    💡 All QSOs must be confirmed and synchronized with LoTW

awards-no-diploma =
    ⚠️ Diploma <b>{ $diploma }</b> incompleted.

    💡 <i>Probably may not have uploaded the LoTW report file.</i>

awards-diploma = 🏆 You have received <b>{ $diploma }</b> #{ $number }.

    💡 <i>You can download the diploma in PDF format.</i>

awards-congrats = 🏆 Congratulations, <b>{ $diploma }</b> #{$number} has been completed.

    💡 <i>You can download the diploma in PDF format.</i>

awards-of = of

awards-pdf = ✅ Download PDF

awards-qrx = 💾 The PDF file will be ready soon... QRX...

pdf-congrats = ✅ The PDF file has been successfully created.

w100c-text = Awarded {$name} for succesfull cofirmation of 2-way radio contacts with amateur radio stations from {$states} countries of the world according to the DXCC list

w100l-text = Awarded {$name} for conducting 2-way radio contacts with amateur radio stations from {$locators} various QTH locators via the QO-100 satellite

w100u-text = Awarded {$name} for conducting 2-way radio unique contacts with {$unique} amateur radio stations via the QO-100 satellite

w100b-text = Awarded {$name} for conducting {$qsos} 2-way QSOs with amateur radio stations via the QO-100 satellite

w25r-text = Awarded {$name} for conducting 2-way contacts with {$rus} regions of Russia via the QO-100 satellite

# -------------------------------------- Other --------------------------------------

back = ⬅️ back
