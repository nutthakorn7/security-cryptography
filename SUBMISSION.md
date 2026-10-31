# คู่มือ Lab Cryptography ทั้ง 10 สัปดาห์และการส่งงาน

คู่มือสำหรับนักศึกษา: วิธีรัน Lab หลัก 10 สัปดาห์ หลักฐานที่ต้องเก็บ และช่องทางส่งงาน ใช้สารบัญเลือกสัปดาห์ที่กำลังเรียนได้ทันที

**Platforms:** the **course platform** (material, quizzes, hand-in) + **GitHub** (your code fixes).

| What | Where |
|---|---|
| Course material — worksheets, lab guides | **`learn.zcr.ai/learn/cryptography`** — no sign-in needed |
| Weekly quiz | **`learn.zcr.ai/quiz`** — the one-time code on your slip |
| Worksheet PDFs, project report | **`learn.zcr.ai/submit`** — the submission code on your slip |
| Code fixes (Wk12) | **GitHub** — your own fork of this course's repo |

> **Hand in on the course platform only.** Google Classroom carries announcements and the weekly
> outline. Nothing is submitted there, and there is no Google Form for this course. The instructor
> keeps copies of what you hand in on the platform as course evidence, so never upload work twice.

This course has its **own** GitHub repo, separate from the companion
`software-security` course's, with its own 20-week, 100-minute timetable and assessment policy.
Fork *this* course's repo; work submitted against the wrong course cannot be graded here. The
platform files every quiz and every hand-in under the course it belongs to, so the code on your
slip is what puts your work in *this* class.

All offensive work is on the provided sandbox targets only — see this course's own ethics &
authorized-use policy, [`ETHICS.md`](ETHICS.md).

---

## One-time setup (Week 1)
**Every lab starts with `cd labs/weekNN-…`, so you need the repository on your own
machine before Week 1. Nothing on the website will work without this step.**

1. Create a GitHub account, then **fork** this course's repo:
   <https://github.com/nutthakorn7/security-cryptography>
2. Clone your fork and check it out:
   ```bash
   git clone https://github.com/<your-github-username>/security-cryptography.git
   cd security-cryptography
   ```
   Then stand up the environment (Docker) per Week 1.
3. Read the material at **`learn.zcr.ai/learn/cryptography/`** — no sign-in needed.
4. Keep the **slip you are given in class**. It carries your quiz code and your submission code;
   those two codes are the only credential you need, and they are what files your work under
   *this* course. There is no account to create and no password to remember.

---

## Weekly LAB — how to do & submit

**Read this before assuming "edit the code, commit a fix" — most weeks in this course don't work
that way.** Unlike `software-security` (which ships a `solution_skeleton.py` per week for you to
complete), this course's `fixed_app.py`/reference-fixed mode is **already fully built** for every
week except one. Most weeks you *confirm* the fix works and *explain why* — you don't write it.

**Do it (most weeks):**
1. Stand up the week's target: `docker compose up` (or the command in that lab's README).
2. Work through the **worksheet** (`labs/week<NN>…/worksheet.md`): for each task record the
   **payload/command**, a **screenshot** of the result, and the requested explanation. The
   "Audit the AI" section does require you to **rewrite a flawed snippet** — but that rewrite goes
   *in the worksheet itself*, not as a code commit.

**Do it (Week 12 only — the one week with a real code-writing task):** in addition to the above,
`alice_student.py` ships with its one fix function stubbed as `raise NotImplementedError`. Write
the real implementation yourself (see that lab's worksheet Part 2a step 5 and the file's own
docstring), verify it against `docker-compose.student-task.yml`, then:
1. In your fork, create a branch `wk12`.
2. Commit your completed `alice_student.py` to that branch and note the **commit hash** in the
   worksheet, alongside your explanation of what each line does.

**Submit:**
| Part | Where | What | Weeks |
|------|-------|------|------|
| Worksheet | **`learn.zcr.ai/submit`** | the completed worksheet exported to **PDF** (screenshots embedded). You can replace it any time before the deadline. | all |
| Code fix | **GitHub** | push branch `wk12`, open a PR (or paste the commit link in the worksheet) | Wk12 only |

**File name:** `Wk<NN>_<StudentID>.pdf`  (e.g. `Wk04_65123456.pdf`)
**Deadline:** 23:59 Thai time (ICT) on the Sunday before the next week's class (KOSEN rule), unless the instructor announces otherwise. The exact date is on `learn.zcr.ai/submit`.
**Late work:** loses 10% of the item's score for each day late (a part day counts as a day), down to 0. The platform takes late uploads for 10 days, until the score would reach 0, and marks them late.
**Grading:** each teaching worksheet is **100 points = common practical 60 + assigned-format 40**.
Common: main task/observations 20 + controls/tests/limitations 20 + reproducible evidence/reasoning 20.
Conventional: ordinary written questions 40. AIR-Sec: Audit-the-AI 20 + Explain-in-Plain-English 10
+ Prompt Problem 10. Complete one assigned 40-point section, not both. The 12 worksheets
(W1–6, W10–15) contribute equally at **2.5 course points each**, totalling 30%.
W1/W10 earn the common 60 through cases, diagrams, experiments or code analysis; no Docker/flag
is required. Viva verifies understanding within the existing rubric, with no additional marks
or automatic fail gate. Preparation/extension items remain available outside the in-class core.

### Flags and evidence, by week type

`course-plan-19weeks.md` classifies the amount of runnable work, not a separate grading rule.
Both worksheet formats submit the common practical evidence.

| Weeks | Activity | Evidence |
|---|---|---|
| W2, W3, W4, W6, W11, W15 | Flag-bearing target | Commands/payloads, actual result and flag where printed, plus fixed/control tests and reasoning |
| W5, W12, W13, W14 | Protocol/log demonstration | Relevant vulnerable/fixed logs, successful/failed control behaviour and explanation |
| W1, W10 | Conceptual/case/code analysis | Case/diagram/experiment or code proof and reasoning; no required Docker target or flag |

Local targets may print a shared placeholder flag; it is not a personalized attribution mechanism.
Use any cohort-specific flag only when actually issued by the instructor. These instructions do
not assert that a CTFd instance or automatic flag checks are live. Put required results in the
worksheet PDF with your name/Student ID and submit through the course platform. The evidence
must be your own; a flag alone does not establish that you performed or understood the task.

---

## คู่มือ Lab ทั้ง 10 สัปดาห์

คู่มือนี้รวบรวม Lab ที่รันได้ของรายวิชา Cryptography: **W02–W06 และ W11–W15** ใช้คู่กับใบงานประจำสัปดาห์ ไม่ใช่เฉลยหรือใบงานทดแทน ส่วน W01/W10 เป็นกิจกรรมแนวคิด, W07/W17 เป็นทบทวน, W08–09/W18–19 เป็นสอบ W16 เป็น CryptoVault studio และ W20 เป็นคืนผล/สะท้อนการเรียนรู้ จึงไม่ใช่ 10 Lab ในรายการนี้

**กติกาส่งงานที่ใช้:** ส่งใบงาน PDF ทุกสัปดาห์ที่ [ส่งงานบนเว็บ](https://learn.zcr.ai/submit) ชื่อ `Wk<NN>_<StudentID>.pdf` ภายในวันอาทิตย์ 23:59 น. (เวลาไทย) ก่อนวันเรียนของสัปดาห์ถัดไป (กติกา KOSEN) เว้นแต่ผู้สอนประกาศเปลี่ยน วันที่แน่นอนดูได้ที่หน้าส่งงาน ส่งช้าหักวันละ 10% ของคะแนนงานนั้น (เกินมาไม่ถึงวันนับเป็นหนึ่งวัน) จนเหลือ 0 เว็บรับงานส่งช้าได้อีก 10 วันหลังกำหนดส่ง เฉพาะ **W12** มีงานแก้โค้ดที่ต้อง commit/ส่งลิงก์ GitHub เพิ่ม หาก README เก่าระบุ GitHub หรือ Classroom ต่างจากหน้านี้ ให้ยึดหัวข้อ Weekly LAB ด้านบนและประกาศผู้สอน Google Classroom ใช้แจ้งข่าวและสรุปรายสัปดาห์เท่านั้น ไม่ต้องส่งงานที่นั่น ผู้สอนเก็บสำเนางานจากเว็บส่งงานไว้เป็นหลักฐานของรายวิชาเอง

### เตรียมเครื่องและวิธีใช้คำสั่ง

ติดตั้ง Git, Docker Desktop หรือ Docker Engine พร้อม Compose v2 และ Python 3 แล้ว fork/clone repository ตาม One-time setup ด้านบน เปิด Docker ให้พร้อมก่อนเริ่ม

จากโฟลเดอร์หลัก `security-cryptography` สร้าง Python environment **ครั้งเดียว** สำหรับรันสคริปต์บนเครื่อง:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests ecdsa
docker compose version
docker info
```

คำสั่งในคู่มือนี้ใช้ terminal แบบ bash/zsh บน macOS/Linux; บน Windows ใช้ WSL2 พร้อมเปิด Docker Desktop integration สำหรับ WSL หรือปรับคำสั่ง activate ให้ตรง shell ของตนเอง เมื่อเปิด terminal ใหม่ ให้กลับมาโฟลเดอร์ repo แล้ว `source .venv/bin/activate` อีกครั้ง ไม่ต้องสร้าง environment ใหม่

**ทุกชุดคำสั่งประจำสัปดาห์เริ่มจากโฟลเดอร์หลักของ repo** หากอยู่ใน `labs/weekNN-...` ของสัปดาห์ก่อน ให้ `cd ../..` ก่อนเลือกสัปดาห์ถัดไป สำหรับ Lab ที่ให้รัน `python exploit.py` สคริปต์รันบนเครื่องของนักศึกษา ส่วน target รันใน Docker; ไม่ต้องติดตั้ง Flask หรือ bcrypt บนเครื่องเพื่อรันสคริปต์เหล่านี้

- **Vulnerable** คือโหมดสำหรับสังเกตปัญหา; **fixed** คือ reference สำหรับเปรียบเทียบผล ยังต้องอ่านข้อจำกัดของแต่ละ demo และอธิบายเหตุผลด้วยตนเอง
- `up -d` รันเบื้องหลัง; ดูความพร้อมด้วย `docker compose ps -a` และ `docker compose logs` การติดตั้ง dependency ใน container ครั้งแรกอาจใช้เวลา
- `logs -f` ติดตาม log ต่อเนื่อง กด **Ctrl-C เพื่อหยุดดู log เท่านั้น** container ยังอยู่ จึงเก็บหลักฐานเพิ่มได้ก่อน `down`
- Lab ที่มี Compose หลายไฟล์ต้องรัน **ทีละโหมดและ `down` โหมดเดิมก่อน** เพราะใช้ชื่อ container ซ้ำกัน
- เก็บหลักฐานก่อน `down`; การเริ่มใหม่จะล้าง state ในหน่วยความจำ เช่นยอดถอนใน W11 ถ้าใช้ `grep -c` แล้วได้ `0` จะมี exit status 1 ตามปกติของ grep ไม่ใช่หลักฐานว่า Lab เสีย และต้องตรวจด้วยว่า client รันจบ/มี log สำเร็จหรือปฏิเสธตามคาด ไม่ใช่ยังไม่เริ่ม
- ใช้เฉพาะ target ที่จัดไว้ใน Lab ตาม [ETHICS.md](ETHICS.md)

### เช็กลิสต์ PDF ที่ใช้ทุกสัปดาห์

1. ชื่อ–รหัสนักศึกษา สัปดาห์ และวันที่ทำงาน
2. คำสั่งหรือ payload ที่ใช้จริง พร้อมผลจาก vulnerable และ fixed ตามใบงาน
3. ภาพหน้าจอหรือ log ที่แสดง flag/ผลลัพธ์ที่สัปดาห์นั้นกำหนด ไม่ใช้เพียงภาพว่า container เปิดอยู่
4. คำอธิบายผลด้วยคำของตนเอง: ทุกคนทำปฏิบัติร่วม 60 คะแนน แล้วทำเฉพาะส่วนที่ได้รับมอบหมาย — Conventional questions 40 หรือ AIR-Sec: Audit-the-AI 20 + EiPE 10 + Prompt Problem 10 ไม่ต้องทำสองรูปแบบรวมกัน รายการด้านล่างเป็นเช็กลิสต์หลักฐาน ไม่ใช่คำถามทั้งหมด
5. เปิดเผยการใช้ AI; viva ใช้ตรวจความเข้าใจภายใต้คะแนนส่วนเดิม ไม่มีคะแนนเพิ่มหรือเกณฑ์ตกอัตโนมัติ

ใช้ชื่อ–รหัสนักศึกษาใน PDF และแสดงคำสั่ง ผลรัน หรือภาพ/log ให้ทำซ้ำและอธิบายได้ทั้งสองรูปแบบ หากงานเฉพาะกำหนดให้ระบุพารามิเตอร์หรือหลักฐานที่ออกให้เฉพาะคน ให้แนบตามโจทย์นั้น ไม่บังคับ identity stamp หรือ flag ส่วนบุคคลกับทุกกิจกรรม Flag ให้บันทึกค่าจากการรันจริง; placeholder ไม่ใช่หลักฐานระบุตัวบุคคล


### ภาพรวมก่อนเริ่ม

| สัปดาห์ | Lab | สิ่งที่เก็บ | ช่องทางหลัก |
|---|---|---|---|
| W02 | Hash: MD5 เทียบ bcrypt | flag + หลักฐาน login/ผล crack | PDF |
| W03 | MACs: length extension เทียบ HMAC | flag + cookie/ผล reject | PDF |
| W04 | AES modes: CBC bit-flipping เทียบ GCM | flag + token/ผล reject | PDF |
| W05 | Key exchange: DH MITM เทียบ authenticated DH | log สองโหมด | PDF |
| W06 | AEAD: padding oracle เทียบ GCM | flag + plaintext/ผล oracle | PDF |
| W11 | ECDSA malleability และ ZKP ในใบงาน | flag + signature/รายการถอน | PDF |
| W12 | TLS certificate validation | log + โค้ด `alice_student.py` | PDF + GitHub |
| W13 | E2E encryption | server/client log สองโหมด | PDF |
| W14 | Authentication: password เทียบ challenge-response | log สองโหมด | PDF |
| W15 | PQC: Lamport one-time signature | flag + หลักฐานการใช้ key ซ้ำ | PDF |


## W02 — Hash: เดารหัสผ่านจาก MD5 และเทียบกับ bcrypt

**เรียนรู้อะไร:** ใช้รายการคำศัพท์โจมตีฐานข้อมูลรหัสผ่านที่เก็บเป็น MD5 โดยไม่มี salt แล้วใช้รหัสผ่านที่หาได้เข้าสู่ระบบ เปรียบเทียบกับฐานข้อมูล bcrypt เพื่ออธิบายผลของ salt และต้นทุนการคำนวณ

เอกสาร: [README](labs/week02-hash/README.md) · [Worksheet](labs/week02-hash/worksheet.md)

**คำสั่งรันจาก repo root:** ต้องมี Docker และ Python พร้อมแพ็กเกจ `requests` บนเครื่องก่อน `exploit.py` รันบนเครื่อง ส่วนแอปเป้าหมายรันใน Docker

```bash
cd labs/week02-hash
docker compose up -d
python exploit.py
```

แอป vulnerable อยู่ที่ `http://localhost:8094` และ fixed อยู่ที่ `http://localhost:8095` เปิดสองบริการไว้ระหว่างทำโจทย์และเก็บหลักฐาน หลังทำครบจึงรัน:

```bash
docker compose down
cd ../..
```

**ผลที่ต้องตรวจ:** สคริปต์แสดงผลการโจมตี vulnerable สำเร็จ ได้ flag และตรวจ fixed ผ่านด้วย exit code `0` จากนั้นทำการทดลองใน worksheet เพิ่มเติม ได้แก่ หา password และจับเวลาคร่าว ๆ ด้วยตนเอง เทียบคำขอที่มี session cookie กับคำขอที่ไม่มี cookie และลองใช้ตาราง MD5 เดิมกับข้อมูล bcrypt แล้วอธิบายผล ไม่ควรสรุปว่า bcrypt ถอดไม่ได้ทุกกรณี

**หลักฐานส่งใน PDF:**

- คำสั่งและภาพผลการหา password พร้อมเวลาที่ใช้โดยประมาณ และบรรทัดโค้ดตรวจ MD5 ที่ worksheet ให้ระบุ
- ผล `exploit.py` พร้อม flag และผลตรวจ vulnerable/fixed
- คำสั่งและผลการเรียก endpoint โดยใช้ cookie jar เทียบกับไม่ส่ง cookie ซึ่งกรณีหลังต้องถูกปฏิเสธ
- ผลทดลองตาราง MD5 กับข้อมูล bcrypt พร้อมคำอธิบายเรื่อง salt, work factor และการตรวจด้วย `checkpw`

## W03 — MACs: Length extension และ HMAC

**เรียนรู้อะไร:** โจมตี MAC แบบ `SHA256(secret || message)` ด้วย length extension และพิสูจน์ว่าการปลอมแบบเดียวกันไม่ผ่าน HMAC-SHA256

เอกสาร: [README](labs/week03-macs/README.md) · [Worksheet](labs/week03-macs/worksheet.md)

**คำสั่งรันจาก repo root:** ต้องมี Docker และ Python พร้อม `requests` บนเครื่อง ใช้ค่าตั้งต้นของ lab เพื่อให้ความยาว secret ตรงกับสมมติฐานของสคริปต์

```bash
cd labs/week03-macs
docker compose up -d
python exploit.py
```

vulnerable อยู่ที่ `http://localhost:8092` และ fixed อยู่ที่ `http://localhost:8093` เก็บหลักฐานและทำคำขอเพิ่มเติมให้ครบก่อนปิด:

```bash
docker compose down
cd ../..
```

**ผลที่ต้องตรวจ:** สคริปต์ใช้ค่าที่ได้รับจากบริการเพื่อสร้างคู่ข้อมูล/ลายเซ็นที่ถูกต่อเติม vulnerable ยอมรับและคืน flag ส่วน fixed ปฏิเสธด้วย HTTP `403` คำนวณ glue padding ด้วยตนเองตาม worksheet และตรวจผลด้วยคำขอ manual ที่ใบงานกำหนด

**หลักฐานส่งใน PDF:**

- ค่า cookie `data`/`sig` ก่อนโจมตี และข้อความหลัง decode ตามโจทย์
- ขั้นตอนคำนวณ glue padding และการแสดงช่วงไบต์ที่ใบงานขอ พร้อมคำอธิบายของตนเอง
- ผลสคริปต์ คู่ข้อมูล/ลายเซ็นที่ปลอมได้ flag และคำสั่ง manual ที่ยืนยันว่า vulnerable ยอมรับ
- ผล fixed ปฏิเสธการปลอม พร้อมอธิบายว่าทำไม HMAC จึงไม่ใช้โครงสร้างแบบ secret-prefix MAC

## W04 — AES Modes: CBC bit-flipping เทียบกับ GCM

**เรียนรู้อะไร:** เปลี่ยนความหมายของข้อมูลที่เข้ารหัสด้วย CBC ผ่านการแก้ ciphertext โดยไม่รู้กุญแจ แล้วเปรียบเทียบกับ AES-GCM ที่ตรวจ authentication tag ก่อนยอมรับข้อมูล

เอกสาร: [README](labs/week04-aes-modes/README.md) · [Worksheet](labs/week04-aes-modes/worksheet.md)

**คำสั่งรันจาก repo root:** ต้องมี Docker และ Python พร้อม `requests` บนเครื่อง การโจมตีในสคริปต์ไม่ต้องติดตั้งไลบรารี AES บนเครื่องเพิ่ม

```bash
cd labs/week04-aes-modes
docker compose up -d
python exploit.py
```

vulnerable อยู่ที่ `http://localhost:8096` และ fixed อยู่ที่ `http://localhost:8097` ทำขั้นตอนใน worksheet และเก็บหลักฐานก่อนปิด:

```bash
docker compose down
cd ../..
```

**ผลที่ต้องตรวจ:** token เดิมแสดงสิทธิ์ guest จากนั้น token ที่ถูกแก้ทำให้ vulnerable ยอมรับสิทธิ์ admin และคืน flag แต่ fixed ปฏิเสธ token ที่ถูกแก้ด้วย HTTP `403` ต้องคำนวณตำแหน่งไบต์และ XOR delta ตาม worksheet เอง พร้อมอธิบายว่าการเข้ารหัสอย่างเดียวไม่รับประกันความถูกต้องของข้อมูล

**หลักฐานส่งใน PDF:**

- token เดิมและผลตรวจสิทธิ์ก่อนแก้
- การคำนวณตำแหน่งและ XOR delta พร้อมเหตุผลว่าการแก้บล็อกก่อนหน้ากระทบ plaintext เป้าหมายอย่างไร
- token หลังแก้ ผลสคริปต์ flag และคำสั่ง manual ที่ยืนยันผลกับ vulnerable
- ผล fixed ปฏิเสธ พร้อมอธิบายบทบาทของ GCM tag และเหตุใดจึงนำตำแหน่งแบบ CBC ไปใช้ตรง ๆ ไม่ได้

## W05 — Key Exchanges: MITM ต่อ Diffie–Hellman

**เรียนรู้อะไร:** สังเกต relay ทำ DH แยกกับ Alice และ Bob เพื่ออ่านและส่งต่อข้อความ เปรียบเทียบกับโหมดที่ Alice/Bob ตรวจ HMAC ของ public key ก่อนสร้าง session key ส่วน small-subgroup attack เป็นงานอธิบายแนวคิดใน worksheet ไม่ใช่การโจมตีที่ demo นี้รัน

เอกสาร: [README](labs/week05-key-exchanges/README.md) · [Worksheet](labs/week05-key-exchanges/worksheet.md)

**คำสั่งรันจาก repo root:** ใช้ Docker ทั้งหมด ไม่ต้องรัน Python client บนเครื่อง และไม่มีพอร์ตที่เปิดให้เข้าผ่าน `localhost` เริ่มจาก vulnerable mode:

```bash
cd labs/week05-key-exchanges
docker compose -f docker-compose.vulnerable.yml up -d --build
docker compose -f docker-compose.vulnerable.yml logs -f
```

เมื่อเห็น log ครบ กด **Ctrl-C เพื่อหยุดการติดตาม log เท่านั้น** จากนั้นเก็บภาพหลักฐาน vulnerable ให้ครบ แล้วปิดชุดนี้ก่อนเริ่ม fixed:

```bash
docker compose -f docker-compose.vulnerable.yml down
docker compose -f docker-compose.fixed.yml up -d --build
docker compose -f docker-compose.fixed.yml logs -f
```

เมื่อเห็นผลของทั้ง Alice และ Bob แล้ว กด **Ctrl-C เพื่อหยุดการติดตาม log เท่านั้น** ตรวจและเก็บหลักฐานคำสั่งต่อไปนี้ **ก่อน** `down`:

```bash
docker compose -f docker-compose.fixed.yml logs | grep -c "RELAY INTERCEPTED"
```

ต้องพิมพ์ `0` เมื่อไม่มีบรรทัดดังกล่าว ทั้งนี้ `grep -c` คืน exit code `1` เมื่อไม่พบข้อความ แม้พิมพ์ `0` ซึ่งเป็นพฤติกรรมปกติสำหรับการตรวจนี้ หลังเก็บหลักฐานทั้งหมดแล้วจึงปิด:

```bash
docker compose -f docker-compose.fixed.yml down
cd ../..
```

**ผลที่ต้องตรวจ:** vulnerable มี log `RELAY: completed independent DH handshake...` สองครั้งก่อน `RELAY INTERCEPTED: ...` และ Bob ได้ข้อความเดียวกัน ส่วน fixed ต้องมี `AUTH FAILED - ABORTING` จาก **ทั้ง Alice และ Bob** ไม่มี `RELAY INTERCEPTED` และการนับข้างต้นได้ `0` การที่ Alice/Bob จบด้วย nonzero ใน fixed mode เป็นผลที่คาดหวังจากการปฏิเสธ MITM

**หลักฐานส่งใน PDF:**

- log vulnerable แบบเห็นลำดับ handshake ทั้งสอง การดักอ่านข้อความ และข้อความที่ Bob ได้รับ พร้อมคำสั่งและบริบทที่ทำซ้ำได้
- คำอธิบายหนึ่งบรรทัดตามโจทย์ว่า relay ต้องทำสอง handshake เพราะอะไร
- log fixed ที่เห็นการปฏิเสธจาก Alice และ Bob พร้อมผล `grep -c` ที่พิมพ์ `0`
- ส่วนเฉพาะรูปแบบที่ได้รับมอบหมาย: Conventional ตอบ Part 1; AIR-Sec ส่ง Audit-the-AI, EiPE เรื่อง small-subgroup และ Prompt Problem พร้อม prompt/คำตอบ AI เต็มฉบับ/คำวิจารณ์ตามใบงาน ทั้งสองแบบส่งปฏิบัติร่วม 60

สัปดาห์นี้ส่ง **หลักฐาน log แทน flag** ไม่ต้องสร้างหรือแก้โค้ด fixed เอง คำสั่ง detached ข้างต้นรองรับโครงสร้าง Compose ปัจจุบัน: Alice อาจทำงานจบไปแล้วเมื่อเริ่มดู log แต่ log ยังอ่านได้จนกว่าจะ `down` บริการทั้งหมดสื่อสารใน Docker network

## W06 — AEAD: Padding oracle เทียบกับ AES-GCM

**เรียนรู้อะไร:** ใช้ความต่างของคำตอบจาก CBC padding oracle เพื่อกู้ plaintext ทีละไบต์ เปรียบเทียบกับ AES-GCM ที่ตรวจ tag และใช้ผลผิดพลาดแบบเดียวกันจนไม่เหลือ oracle ที่ใช้โจมตีแบบนี้ได้

เอกสาร: [README](labs/week06-aead/README.md) · [Worksheet](labs/week06-aead/worksheet.md)

**คำสั่งรันจาก repo root:** ต้องมี Docker และ Python พร้อม `requests` บนเครื่อง สคริปต์โจมตีส่ง HTTP จำนวนมาก จึงควรรอจนทำงานจบ

```bash
cd labs/week06-aead
docker compose up -d
python exploit.py
```

vulnerable อยู่ที่ `http://localhost:8098` และ fixed อยู่ที่ `http://localhost:8099` เก็บหลักฐานและทำคำขอ manual ใน worksheet ก่อนปิด:

```bash
docker compose down
cd ../..
```

**ผลที่ต้องตรวจ:** vulnerable เปิดเผยความต่างของผลตรวจ padding ผ่านสถานะ HTTP ทำให้สคริปต์กู้ plaintext และ flag ได้ ส่วน fixed ไม่ให้สัญญาณที่ใช้กู้ข้อความด้วยการโจมตีนี้ได้ ตรวจจำนวนบล็อกจาก ciphertext ของตนเอง และอธิบายการทดสอบหนึ่งคำขอรวมถึงการตรวจซ้ำเพื่อกรอง false positive ตามใบงาน

**หลักฐานส่งใน PDF:**

- ciphertext ที่ได้ ความยาว และจำนวนบล็อกหลังแยก IV ตามที่ worksheet ขอ
- ผลสคริปต์ที่กู้ plaintext และ flag จาก vulnerable
- คำสั่ง manual ที่เรียก oracle พร้อมสถานะตอบกลับ และคำอธิบายความหมายของผลนั้น
- ผลทดสอบ fixed ที่ไม่สามารถใช้ response เป็น padding oracle ได้ พร้อมอธิบายลำดับตรวจ tag และการตอบข้อผิดพลาด

## W11 — Signatures & Zero-Knowledge Proofs

**ทำอะไร:** ทดลอง ECDSA signature malleability ว่า authorization เดิมถูกนับซ้ำได้อย่างไร เมื่อระบบแยกรายการจาก hash ของลายเซ็น แล้วเปรียบเทียบ reference ที่ปฏิเสธ high-S twin ส่วน ZKP เป็นกิจกรรมอธิบายในใบงาน

[อ่านใบงาน W11](labs/week11-signatures-zkp/worksheet.md) · [README W11](labs/week11-signatures-zkp/README.md)

**รันจาก repo root:**

```bash
cd labs/week11-signatures-zkp
docker compose up -d
```

ทำ Tasks 1–3 ในใบงานด้วยมือก่อน `exploit.py` โดยเริ่มจาก container ใหม่ เก็บคำสั่งและ JSON ที่แสดงยอด `100` แล้ว `200` จากคู่ลายเซ็นตามโจทย์ จากนั้นเริ่ม state ใหม่ก่อนตรวจซ้ำอัตโนมัติ:

```bash
docker compose down
docker compose up -d
python exploit.py
# เก็บผล vulnerable และ fixed ก่อนหยุด
docker compose down
```

Vulnerable ใช้ `localhost:8102`; fixed ใช้ `localhost:8103` อย่ารันสคริปต์ก่อนชุดหลักฐานด้วยมือ เพราะยอดถอนและรายการที่เคยใช้จะอยู่จน container หยุด

**ตรวจผลและส่งใน PDF:** คู่ `(r,s)` กับ `(r,n-s)`, การคำนวณ `s'` และ txid ทั้งสอง, คำสั่ง `curl`/JSON ที่แสดง `total_withdrawn:200` และ `double_spend_detected`, flag ที่ได้จริง และผล fixed รับ low-S ครั้งแรกแต่ปฏิเสธ high-S twin ด้วย 403 พร้อมคำอธิบาย

**ขอบเขตที่ต้องอธิบาย:** low-S เลือกหนึ่งตัวจากคู่ลายเซ็น `(r,s)`/`(r,n-s)` ไม่ได้ทำให้ข้อความกับ key หนึ่งคู่มีลายเซ็นที่ถูกต้องได้เพียงค่าเดียวตลอดไป การทดลองนี้เริ่มจาก authorization หนึ่งรายการตามโจทย์

## W12 — Secure Transport / TLS

**ทำอะไร:** เปรียบเทียบ client ที่ยอมรับ certificate ของผู้แอบอ้าง กับ client ที่ตรวจ trust chain และ hostname แล้วเติมฟังก์ชันตรวจ certificate ของตนเอง นี่คือสัปดาห์เดียวในคู่มือนี้ที่ต้องส่งโค้ดแก้จริง

[อ่านใบงาน W12](labs/week12-secure-transport/worksheet.md) · [README W12](labs/week12-secure-transport/README.md)

**รันจาก repo root — vulnerable:**

```bash
cd labs/week12-secure-transport
docker compose -f docker-compose.vulnerable.yml up -d --build
docker compose -f docker-compose.vulnerable.yml logs -f
# หลัง client ทำงานและเก็บหลักฐานแล้ว กด Ctrl-C หยุดดู log
docker compose -f docker-compose.vulnerable.yml down -v
```

**เทียบ fixed:**

```bash
docker compose -f docker-compose.fixed.yml up -d --build
docker compose -f docker-compose.fixed.yml logs -f
# เมื่อเห็นผลปฏิเสธ certificate แล้ว กด Ctrl-C
docker compose -f docker-compose.fixed.yml logs | grep -c "MITM INTERCEPTED"
# เก็บหลักฐานก่อนล้าง demo certificates
docker compose -f docker-compose.fixed.yml down -v
```

**งานโค้ด:** สร้าง branch `wk12` ใน fork ของตนเอง แล้วเขียน `build_client_context()` ใน `alice_student.py` ตามใบงานและ docstring ให้เชื่อถือ demo CA ที่กำหนดและตรวจ hostname จากนั้นทดสอบ:

```bash
git switch -c wk12
# แก้ alice_student.py ด้วย editor ก่อนรันชุดนี้
docker compose -f docker-compose.student-task.yml up -d --build
docker compose -f docker-compose.student-task.yml logs -f
# เก็บหลักฐาน client ปฏิเสธ certificate แล้ว กด Ctrl-C
docker compose -f docker-compose.student-task.yml down -v
git add alice_student.py
git commit -m "Complete W12 certificate validation"
git rev-parse HEAD
git push -u origin wk12
```

ถ้ามี branch `wk12` อยู่แล้ว ใช้ `git switch wk12` แทนการสร้างซ้ำ เปิด PR หรือแนบ commit link ตาม Weekly LAB ด้านบน `down -v` ในชุดนี้ลบ volume certificate ที่สร้างสำหรับ Lab เพื่อไม่ให้ certificate เก่าค้างข้ามโหมด เก็บหลักฐานก่อนลบเสมอ

**ตรวจผลและส่ง:** PDF ต้องมี vulnerable log `MITM INTERCEPTED:` ที่อ่านข้อความได้, fixed/student log `CERT VERIFICATION FAILED - ABORTING` พร้อมเหตุผล certificate ไม่ได้รับความเชื่อถือ, ผลนับ `MITM INTERCEPTED` เป็น `0` ใน fixed, คำอธิบายว่า encryption อย่างเดียวไม่ยืนยันตัวตน server และ diff/ฟังก์ชันที่เขียนพร้อมอธิบายแต่ละบรรทัด ใส่ commit hash และลิงก์ PR/commit ของ `alice_student.py` ใน PDF ด้วย

TLS port `8443` อยู่ภายใน Docker network ไม่ต้องเปิด browser ที่ port นี้บนเครื่อง การที่ client ออกด้วย exit 1 หลังปฏิเสธ certificate เป็นผลที่คาดหมาย ต้องดูข้อความปฏิเสธที่ระบุไว้ ไม่ใช่ยอมรับ Python traceback หรือปิด validation เพื่อให้ login ผ่าน

## W13 — End-to-End Encryption

**ทำอะไร:** สังเกตว่า provider เห็น plaintext เมื่อใด แล้วเปรียบเทียบการเข้ารหัสฝั่ง client ซึ่งทำให้ server เห็น ciphertext ขณะที่ Bob ถอดข้อความได้

[อ่านใบงาน W13](labs/week13-e2e-encryption/worksheet.md) · [README W13](labs/week13-e2e-encryption/README.md)

**รันจาก repo root:**

```bash
cd labs/week13-e2e-encryption
docker compose -f docker-compose.vulnerable.yml up -d --build
docker compose -f docker-compose.vulnerable.yml logs -f
# หลังเห็น SERVER SAW และ BOB RECEIVED เก็บหลักฐานแล้ว Ctrl-C
docker compose -f docker-compose.vulnerable.yml down

docker compose -f docker-compose.fixed.yml up -d --build
docker compose -f docker-compose.fixed.yml logs -f
# หลังเห็น BOB DECRYPTED เก็บหลักฐานแล้ว Ctrl-C
docker compose -f docker-compose.fixed.yml logs server | grep -c "meet at pier 39 at midnight"
docker compose -f docker-compose.fixed.yml down
```

**ตรวจผลและส่งใน PDF:** vulnerable มี `SERVER SAW:` เป็นข้อความอ่านได้และ `BOB RECEIVED:`; fixed มี `SERVER SAW:` เป็น ciphertext/base64 แต่ `BOB DECRYPTED:` อ่านข้อความเดิมได้ ผลค้นหา plaintext ใน **server log เท่านั้น** เป็น `0` พร้อมอธิบายว่าใครถือ key และใครเห็น plaintext ในแต่ละโหมด

บริการใช้ port `8080` ภายใน Docker ไม่มี host port ให้เปิด browser Demo นี้จำลองขอบเขต TLS-only เทียบ E2EE โดยไม่ได้เปิด TLS จริง และยังเชื่อถือ public key ที่ server ส่งให้ Alice จึงต้องแยกคำถามเรื่องความถูกต้องของ public key ออกจากการซ่อนข้อความใน log

## W14 — User Authentication

**ทำอะไร:** เปรียบเทียบการส่ง password ตรง ๆ กับ simplified challenge-response ที่ส่ง nonce/proof แล้วอภิปรายทางเลือก authentication ในใบงาน ได้แก่ PAKE, TOTP, FIDO2/WebAuthn และ SSO

**ไม่ต้องมีอุปกรณ์ FIDO สำหรับรัน Lab นี้** FIDO2/WebAuthn เป็นหนึ่งหัวข้อเปรียบเทียบ ตัว demo หลักรัน client/server ใน Docker

[อ่านใบงาน W14](labs/week14-authentication/worksheet.md) · [README W14](labs/week14-authentication/README.md)

**รันจาก repo root:**

```bash
cd labs/week14-authentication
docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit
# client จบแล้ว stack หยุด เก็บ log ก่อน down
docker compose -f docker-compose.vulnerable.yml down

docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit
# เก็บผล LOGIN OK และ nonce/proof ก่อนตรวจ log
docker compose -f docker-compose.fixed.yml logs | grep -c "correct-horse-battery"
docker compose -f docker-compose.fixed.yml logs | grep -c "SERVER SAW PASSWORD"
docker compose -f docker-compose.fixed.yml down
```

**ตรวจผลและส่งใน PDF:** vulnerable มี `SERVER SAW PASSWORD:` และ `LOGIN OK`; fixed มี `SERVER SAW: nonce=... proof=...` และ `LOGIN OK` พร้อมผล `grep -c` ทั้งสองรายการเป็น `0` อธิบายว่า password อยู่ฝั่งใด ข้อมูลใดเดินทางผ่าน network และใครเห็นอะไร

โหมด fixed นี้แสดงเพียงว่า **ไม่ได้ส่ง password ตรง ๆ** ไม่ใช่ PAKE สมบูรณ์ และการไม่เห็น password ตัวอักษรใน log ไม่ได้พิสูจน์ว่าผู้ถือ transcript เดารหัสผ่านแบบ offline ไม่ได้ หลีกเลี่ยงการสรุปเกินขอบเขตของ demo บริการใช้ port `8080` ภายใน Docker ไม่มี host port

## W15 — Post-Quantum Cryptography / Lamport OTS

**ทำอะไร:** สังเกตความเสียหายจากใช้ Lamport one-time signing key ซ้ำ แล้วเปรียบเทียบ reference ที่ยอมให้เซ็นเพียงครั้งเดียว เชื่อมผลกับแนวคิด hash-based signatures และ crypto-agility

[อ่านใบงาน W15](labs/week15-pqc/worksheet.md) · [README W15](labs/week15-pqc/README.md)

**รันจาก repo root:**

```bash
cd labs/week15-pqc
docker compose up -d
python exploit.py
# เก็บผลและทำใบงานก่อนหยุด
docker compose down
```

Vulnerable ใช้ `localhost:8100`; fixed ใช้ `localhost:8101`

**ตรวจผลและส่งใน PDF:** flag ที่ได้จริง, preimages ทั้งสองค่าของอย่างน้อยหนึ่ง bit พร้อมตรวจ SHA-256 เทียบ public key ตามใบงาน, คำสั่งและผล `/admin`, หลักฐาน fixed ปฏิเสธการเซ็นครั้งที่สองด้วย 403 และคำอธิบายว่าเหตุใดคำว่า one-time จึงเป็นข้อกำหนดของ scheme

**ทางเลือก HNDL:** ภายใน `labs/week15-pqc/hndl/` มี companion Lab เรื่อง harvest-now-decrypt-later ใช้เมื่อผู้สอนเลือกมอบหมายเพิ่มหรือให้เลือกแทน ไม่ใช่งานเพิ่มที่ทุกคนต้องทำโดยอัตโนมัติ

```bash
# เริ่มจาก repo root
cd labs/week15-pqc/hndl
docker compose up -d
python -m pip install -r requirements.txt
python exploit.py
# เก็บ capture/ผลเปรียบเทียบตามใบงาน HNDL ก่อนหยุด
docker compose down
```

อ่าน README/worksheet ในโฟลเดอร์ HNDL ก่อนทำ ใช้ ports `8120/8121`; tiny RSA จำลองการที่ classical KEM ถูกทำลายในภายหลัง ไม่ได้รัน Shor จริง ส่ง capture, ผล classical เทียบ hybrid และคำอธิบายตามใบงานเมื่อได้รับมอบหมาย

### ก่อนกดส่ง

ตรวจว่า PDF มีหลักฐานตามสัปดาห์นั้นครบ มีคำสั่ง/ผลและบริบทที่ทำซ้ำได้ อธิบาย vulnerable/fixed และข้อจำกัดด้วยตนเอง ทำปฏิบัติร่วม 60 และส่วนเฉพาะรูปแบบ 40 ที่ได้รับมอบหมายครบ ใส่ AI disclosure และใช้ชื่อไฟล์ `Wk<NN>_<StudentID>.pdf` สำหรับ W12 ตรวจเพิ่มว่าลิงก์ commit/PR เปิดได้และตรงกับโค้ดที่ทดสอบ แล้วส่งที่ [learn.zcr.ai/submit](https://learn.zcr.ai/submit) ด้วย submission code บน slip ของตนเอง


---

## QUIZ — how it works
- **On the course platform:** go to **`learn.zcr.ai/quiz`** and enter the **one-time code** on
  your slip. The code is yours alone and works once.
- **Weekly quiz:** a short **~10-min quiz at the start of teaching weeks after W1 orientation** (6 Q: 5 MCQ + 1 short, **individual**). Low-stakes — the **lowest 1–2 are dropped**.
- **Cumulative review quizzes:** two bigger 25-pt quizzes in the **review weeks** (W7 pre-midterm, W17 pre-final).
- No separate file to submit — the quiz **is** the submission. Questions come one at a time and
  the quiz only moves forward, so answer each one before you continue.

---

## EXAMS

Every exam session fits **100 minutes**. Written exams and the midterm practical are individual;
the final practical is in teams of 3 (or 2 where needed).

| Exam | Covers | Time, weight and hand-in |
|---|---|---|
| W8 Midterm written | W1–6 | 90-minute paper + 10-minute administration; 8 course points; paper or instructor-assigned quiz |
| W9 Midterm practical | W1–6 | 80-minute practical + 20-minute brief/submission; 12 course points; evidence PDF (evidence, payload and mitigation) through the submission platform |
| W18 Final written | Cumulative, emphasis W10–16 | 90-minute paper + 10-minute administration; 10 course points; paper or instructor-assigned quiz |
| W19 Team final practical | Cumulative, emphasis W10–16 | 80-minute practical + 20-minute brief/submission; 15 course points; evidence PDF through the submission platform |

Midterm totals 20 and final totals 25 course points. Project Q&A is in W16/W20; it does not share
the W19 practical's 100 minutes.

## TERM PROJECT — CryptoVault

- Teams of 3; teams of 2 where necessary for class enrolment. Project weight: **15%**.
- Use [project/REPORT-TEMPLATE.md](project/REPORT-TEMPLATE.md), export the report to PDF and submit
  through the course platform. Link the team's GitHub code, design and self-audit.
- Milestones: W4 team/design → W7 KDF+AEAD → W11 sharing → W14 transport/self-audit → W16 studio.
- Submit the final report/code and a **video of at most 5 minutes before W19**. Put the video link
  (unlisted YouTube, or Google Drive viewable by anyone with the link) in the report PDF. Project clarification
  takes place in W16/W20; no live project demonstration is added to the W19 exam.
- The existing optional crypto-agility bonus is +5 raw points capped at 100. HNDL is optional and
  adds no new mandatory marks. See [project/README.md](project/README.md) for the full rubric.

---

## Rules for every submission
- **Name + Student ID** on every file; teamwork only where stated (worksheets/quizzes/written exams/midterm practical are individual; final practical is team work and CryptoVault is team-graded with peer-contribution scaling — see `project/README.md`).
- **AI-tool disclosure:** state how you used any AI tool (search, code, translate) — a section is built into the worksheet/report.
- **Late:** −10% of the item's score for each day late (a part day counts as a day), down to 0 (see `syllabus.md`); submit what you have.

---

## Academic Integrity & Anti-Cheating

Submit your own evidence and reasoning. Discussing concepts and helping a classmate debug their
own setup are allowed. Disclose AI assistance; do not submit another student's answers, code,
screenshots or flags as your own. Team work is allowed only for the final practical and project.

Name and Student ID belong on every PDF. Include commands/results and enough context to reproduce
the required task. Task-specific issued flags/parameters apply only when actually assigned;
automatic personalized flags, screenshot stamps and code-similarity enforcement are not assumed
for every activity. W12's code must be attributable to the student's own fork/commit.

The instructor may ask you to reproduce or explain a result. Such checks verify the submitted
work within its existing rubric, with no additional viva score or automatic fail gate.
Violations follow [ETHICS.md](ETHICS.md) and KOSEN's academic-integrity process.
