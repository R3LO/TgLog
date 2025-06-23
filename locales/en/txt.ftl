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

reg-cancel = ⛔️ Operation is cancelled.
    To continue run /start

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

convert-log = 📙 Convert any ADIF log

wipe-log = 🗑 Wipe log

worked-statistics = 📊 Log info

my-awards = 🏆 Awards

users-raitings = 📈 Ranking

profile = 💼 Profile

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

# -------------------------------------- Log Info --------------------------------------

log-title = 📡 Statistics on the <b>{$user}</b> log

log-mode = ✅ <b>By modes in the main log:</b>

log-info1 = ✅ Total QSOs in the log:  <b>{$qso}</b>
    ▫️ unique callsigns:  <b>{$uqso}</b>


log-info2 = ✅ Total LoTW CFM:  <b>{$lotws}</b>
    ▫️ unique LoTW callsigns:  <b>{$uniq_lotw}</b>
    ▫️ LoTW confirmability:  <b>{$percent}</b> %

log-info3 = ✅ <b>For Awards on 🛰 QO-100</b>

log-loc = confirmed QRA locators from LoTW

loc-file = 💾 TXT-file with the list of confirmed locations is below 👇

# -------------------------------------- Wipe Log --------------------------------------

wipe-title =
    ⚠️ <b>Do you really want to wipe up the log?</b>

    1️⃣ All statistics will be reset.
    2️⃣ Any diplomas will be not available
    3️⃣ You can upload the logs again at any time.

    💡 <b>If you want to wipe up the log, select the action...</b>

    ▫️ <b>Main log</b> - clears the main log
    ▫️ <b>LoTW Upload</b> - clears downloaded LoTW entries.
    ▫️ <b>All logs</b> - clears all records

wipe-all-res = ✅ <b>All your logs have been cleared!</b>

    <i>You can upload the logs again at any time.</i>

wipe-main-res = ✅ <b>Your main logs have been cleared!</b>

    <i>You can upload the log again at any time.</i>

wipe-lotw-res = ✅ <b>Your LoTW entries have been cleared!</b>

    <i>You can upload the LoTW entries again at any time.</i>

wipe-mainlog = ❌ Main log
wipe-lotw = ❌ LoTW Upload
wipe-all = ❌ All logs

# -------------------------------------- Convert --------------------------------------

convert-title = <b>ADIF Converter 🛰 QO-100</b>
    ⭐️ The uploaded file is not uploaded to the main database during conversion. You will receive the converted file in ADIF format.

    <b>The ADIF file should contain the following tags:</b>
    ▫️ QSO_DATE - date of the QSO
    ▫️ TIME_ON - the start time of the QSO
    ▫️ CALL sign of the correspondent
    ▫️ MODE - type of communication
    ▫️ SUBMODE is a subspecies of communication, an optional field for digital types.
    ▫️ GRIDSQUARE - correspondent's locator (optional field)
    ▫️ After conversion, all BAND tags will be set to <b>13CM</b>
    additional tags are added as <b>PROP_MODE with the value SAT</b> and <b>SAT_NAME with the value QO-100</b>.

    ⭐️ <b>To start file conversion, click on 📎 or drag the ADIF file into this message.</b>

    If you want to abort the conversion, run /cancel

convert-cancel = ⛔️ ADIF conversion canceled.

convert-bigfile = ⛔️ The file size exceeds 10MB.

convert-wrongfile = ❌ Wrong ADIF. It is not an ADIF file.

convert-uploaded = ✅ Uploaded <b>{$sum_qso}</b> QSO.

convert-ready = 💾 The ADIF file has been converted 👇

# -------------------------------------- Menu Upload --------------------------------

upload-title = ⭐️ Uploaded files must be no more than <b>10MB</b> at a time.
    ⭐️ The format of the uploaded files <b>is ADIF</b>.
    ⭐️ Dupe entries are not included in the log.
    ⭐️ Entries are uploader only for band <b>13CM</b>.

upload-main-log = 📘 Main log

upload-lotw-sync = 📗LoTW sync

upload-file = ⭐️ <i><b>The file's ADIF must contain tags:</b></i>

    ▫️QSO_DATE ▫️TIME_ON ▫️CALL ▫️MODE ▫️BAND = 13CM

    💾 <b>To start downloading, click on 📎 or drag the log file into this message.</b>

    ⚠️ <i>To cancel the download, send /cancel</i>

upload-bigfile = ⛔️ The file size is too large.

upload-cancel = ⛔️ Downloading has been canceled.

upload-ok = 💡 The main log is uploaded.

upload-wrong = ❌ Wrong ADIF file.

upload-found-qso = ✅  <b>{$sum_qso}</b> QSO found. QRX...

upload-errors = ❌ <b>Errors occurred when processing the file.</b>

    💾 <i>QSOs that was not included in the database is in the attached file below 👇 </i>

upload-db = ✅ <b>{$n}</b> QSOs for the 13CM band have been added to the database.

# -------------------------------------- Menu Download --------------------------------

download-title = ❓ <b>What format do you want to download the log in?</b>
    1️⃣ CSV can be opened in Excel
    2️⃣ ADIF can be uploaded to other logs

download-csv = 💾 CSV file

download-adif = 💾 ADIF file

download-file = 📌 <b>{$user}</b> in the log <b>{$qsos}</b> QSO.
    💾 The ADIF file has been created 👇

download-file2 = 📌 <b>{$user}</b> in the log <b>{$qsos}</b> QSO.
    💾 The CSV file has been created 👇

download-nothing = ❌ Nothing to download!

# -------------------------------------- Other --------------------------------------

back = ⬅️ back

# -------------------------------------- Menu Help --------------------------------------

help-text =
    📡 Telegram bot 🤖 <b>TLog 2.0</b> is your hardware crane for working with the QO-100 satellite.

    🔸 <b>Main functions:</b>
    - Log upload and synchronization with LoTW
    - Saving the log in CSV and ADIF format with the necessary tags for QO-100
    - Search for connections by call sign and QTH locators
    - User rating - Diploma program QO-100-RUSSIA
    - Conversion of any ADIF into a file with tags for QO-100
    - Preparation of an extract for the CPR Cosmos diploma

    🔸 <b>Log function</b>
    - Texting a part of the call sign or locators to search for svsi by text message
    - Texting a spot message from the QO-100-RUSSIA DXSpot group to the Tlog

    🔸 <b>Loading the main log and sync LoTW</b>
    - Create an ADIF file and upload it to the main log.
    - To synchronize with LoTW, download the full lotwreport.adi file and upload it

    🔸 <b>User rating</b>
    - Provides a rating of TLog users in various categories

    🔸 <b>Awards</b>
    - Diplomas for the QO-100-RUSSIA diploma program are issued and recorded based on LoTW data and the main log that must be uploaded.

    🔸 <b>Log statistics</b>
    - Basic information about your log

    🔸 <b>Profile</b>
    - Allows you to change your name, which is indicated on the diplomas issued

    🔸 <b>Utilities</b>
    - Conversion of the ADIF log
    - Formation of a diploma statement from CPR Coamos
    - Download paper QSL cards to confirm the countries or regions of Russia required for the diploma program.

    🔸 <b>Clearing the log</b>
    - You can clear only the main log, only the data from LoTW, or the whole thing

    🔸 <b>QO-100-RUSSIA</b>
    - Telegram group QO-100-RUSSIA with the theme DX Spots for DX hunters