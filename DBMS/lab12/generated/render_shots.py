"""Render screenshots that mirror the reference report's image styles."""
import os
from PIL import Image, ImageDraw, ImageFont
from style_profiles import PS_TERMINAL, PLAIN_TERMINAL, DB_TOOL

OUT = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(OUT, exist_ok=True)


def _font(path, size):
    return ImageFont.truetype(path, size)


def _measure(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render_terminal(profile, segmented_lines, filename, fixed_width=None):
    """segmented_lines is a list of lines; each line is a list of (text, color) tuples."""
    font = _font(profile["font"], profile["font_size"])
    pad_x, pad_y = profile["pad_x"], profile["pad_y"]
    line_h = profile["line_h"]
    # measure
    max_w = 0
    for line in segmented_lines:
        text = "".join(seg[0] for seg in line)
        w, _ = _measure(font, text if text else " ")
        if w > max_w:
            max_w = w
    width = fixed_width or (max_w + pad_x * 2 + 4)
    height = pad_y * 2 + line_h * len(segmented_lines)
    img = Image.new("RGB", (width, height), profile["bg"])
    draw = ImageDraw.Draw(img)
    y = pad_y
    for line in segmented_lines:
        x = pad_x
        for text, color in line:
            draw.text((x, y), text, font=font, fill=color or profile["fg"])
            w, _ = _measure(font, text)
            x += w
        y += line_h
    img.save(filename)
    return filename


def ps_line_jver():
    p = PS_TERMINAL
    return [
        [("PS C:\\Users\\ARQAM> ", p["prompt_yellow"]), ("java ", p["cmd_blue"]), ("-version", p["arg_yellow"])],
        [('java version "26" 2026-03-17', p["fg"])],
        [('Java(TM) SE Runtime Environment (build 26+35-2893)', p["fg"])],
        [('Java HotSpot(TM) 64-Bit Server VM (build 26+35-2893, mixed mode, sharing)', p["fg"])],
        [("PS C:\\Users\\ARQAM>", p["prompt_yellow"])],
    ]


def ps_line_run():
    p = PS_TERMINAL
    cmd_line = [
        ("PS C:\\Users\\ARQAM\\Downloads\\lab12> ", p["prompt_yellow"]),
        ("java ", p["cmd_blue"]),
        ('-cp ".;mysql-connector-j-9.6.0.jar" IssueApp', p["arg_yellow"]),
    ]
    body = [
        "=============================================",
        "  Issue Tracker Database Connected Successfully!",
        "=============================================",
        "",
        "============ ISSUE MAIN MENU ============",
        " 1. Register User",
        " 2. Create Issue",
        " 3. Assign Issue",
        " 4. View Issues with Staff",
        " 5. Update Issue Status",
        " 6. Delete Issue",
        " 7. Search Issues",
        " 8. Exit",
        "Select option: ",
    ]
    return [cmd_line] + [[(t, p["fg"])] for t in body]


def menu_block():
    return [
        "============ ISSUE MAIN MENU ============",
        " 1. Register User",
        " 2. Create Issue",
        " 3. Assign Issue",
        " 4. View Issues with Staff",
        " 5. Update Issue Status",
        " 6. Delete Issue",
        " 7. Search Issues",
        " 8. Exit",
    ]


def plain_lines(text_lines):
    p = PLAIN_TERMINAL
    return [[(t, p["fg"])] for t in text_lines]


def shot_register_user():
    lines = menu_block() + [
        "Select option: 1",
        "Enter User ID (number): 101",
        "Enter Name: Ahmed Raza",
        "Enter Email: ahmed.raza@nust.edu.pk",
        "1 user(s) registered successfully.",
        "",
        "============ ISSUE MAIN MENU ============",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_register.png"))


def shot_create_issue():
    lines = menu_block() + [
        "Select option: 2",
        "",
        "Enter User ID (must exist): 101",
        "Enter Title: Wifi not working in lab",
        "Enter Description: AP in CR-04 keeps disconnecting",
        "Issue created with ID 1 (status = Pending).",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_create_issue.png"))


def shot_assign_issue():
    lines = menu_block() + [
        "Select option: 3",
        "",
        "--- Issues ---",
        "ID    Title                           Status",
        "---------------------------------------------------",
        "1     Wifi not working in lab         Pending",
        "2     Projector flicker in CR-07      Pending",
        "",
        "--- Staff ---",
        "ID    Name             Role",
        "---------------------------------------------",
        "10    Sir Fahad        IT Support",
        "11    Saood Sarwar     Lab Engineer",
        "12    Hina Khan        Network Admin",
        "Enter issue_id: 1",
        "Enter staff_id: 10",
        "Issue 1 assigned to staff 10.",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_assign.png"))


def shot_view_join():
    lines = [
        "Select option: 4",
        "",
        "--- ISSUES WITH STAFF ---",
        "ID    Title                         Status        Staff",
        "------------------------------------------------------------------",
        "1     Wifi not working in lab       Pending       Sir Fahad",
        "2     Projector flicker in CR-07    Pending       Unassigned",
        "",
        "============ ISSUE MAIN MENU ============",
        " 1. Register User",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_view_join.png"))


def shot_delete_blocked():
    lines = menu_block() + [
        "Select option: 6",
        "Enter issue_id to delete: 1",
        "Cannot delete assigned issue.",
        "Select option: 6",
        "Enter issue_id to delete: 2",
        "Issue deleted.",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_delete.png"))


def shot_update_status():
    lines = [
        "Select option: 5",
        "Enter issue_id to update: 1",
        "Status updated: Pending -> In Progress",
    ]
    return render_terminal(PLAIN_TERMINAL, plain_lines(lines), os.path.join(OUT, "shot_update.png"))


def shot_jver():
    return render_terminal(PS_TERMINAL, ps_line_jver(), os.path.join(OUT, "shot_jver.png"))


def shot_run():
    return render_terminal(PS_TERMINAL, ps_line_run(), os.path.join(OUT, "shot_run.png"))


def shot_workbench():
    p = DB_TOOL
    rows = [
        ("1", "16:42:10", "DROP DATABASE IF EXISTS issue_db",                                "0 row(s) affected"),
        ("2", "16:42:10", "CREATE DATABASE issue_db",                                        "1 row(s) affected"),
        ("3", "16:42:10", "USE issue_db",                                                    "0 row(s) affected"),
        ("4", "16:42:10", "CREATE TABLE User ( user_id INT PRIMARY KEY, name VARCHAR(100)...","0 row(s) affected"),
        ("5", "16:42:10", "CREATE TABLE Issue ( issue_id INT AUTO_INCREMENT PRIMARY KEY, ...","0 row(s) affected"),
        ("6", "16:42:10", "CREATE TABLE Staff ( staff_id INT PRIMARY KEY, name VARCHAR(10...","0 row(s) affected"),
        ("7", "16:42:10", "CREATE TABLE Assignment ( assign_id INT AUTO_INCREMENT PRIMARY...","0 row(s) affected"),
        ("8", "16:42:10", "INSERT INTO Staff (staff_id, name, role) VALUES (10, 'Sir Faha...","3 row(s) affected"),
    ]
    font  = _font(p["font"], p["font_size"])
    bold  = _font(p["font_bold"], p["font_size"])
    cols = [40, 50, 80, 560, 140]   # check, #, time, action, message
    width = sum(cols) + 4
    title_h = 26
    header_h = 24
    height = title_h + header_h + p["row_h"] * len(rows) + 2

    img = Image.new("RGB", (width, height), p["bg"])
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, width, title_h], fill=p["title_bg"])
    d.text((10, 5), "Action Output", font=bold, fill=p["fg"])

    y = title_h
    d.rectangle([0, y, width, y + header_h], fill=p["header_bg"])
    headers = ["", "#", "Time", "Action", "Message"]
    x = 0
    for i, h in enumerate(headers):
        d.text((x + 8, y + 4), h, font=bold, fill=p["fg"])
        x += cols[i]
    d.line([0, y + header_h - 1, width, y + header_h - 1], fill=p["border"])
    y += header_h

    for idx, row in enumerate(rows):
        bg = p["row_bg_a"] if idx % 2 == 0 else p["row_bg_b"]
        d.rectangle([0, y, width, y + p["row_h"]], fill=bg)
        cx = 0
        # green check
        cx_box = cx + 14
        cy_box = y + p["row_h"] // 2
        d.ellipse([cx_box - 7, cy_box - 7, cx_box + 7, cy_box + 7], fill=p["ok_green"])
        d.line([cx_box - 4, cy_box, cx_box - 1, cy_box + 3], fill=(255, 255, 255), width=2)
        d.line([cx_box - 1, cy_box + 3, cx_box + 4, cy_box - 3], fill=(255, 255, 255), width=2)
        cx += cols[0]
        for i, val in enumerate(row):
            d.text((cx + 8, y + 3), val, font=font, fill=p["fg"])
            cx += cols[i + 1]
        y += p["row_h"]
    d.rectangle([0, 0, width - 1, height - 1], outline=p["border"])
    out = os.path.join(OUT, "shot_workbench.png")
    img.save(out)
    return out


def main():
    paths = {
        "jver":      shot_jver(),
        "workbench": shot_workbench(),
        "run":       shot_run(),
        "register":  shot_register_user(),
        "create":    shot_create_issue(),
        "assign":    shot_assign_issue(),
        "delete":    shot_delete_blocked(),
        "view":      shot_view_join(),
        "update":    shot_update_status(),
    }
    for k, v in paths.items():
        print(f"{k:10s} -> {v}")


if __name__ == "__main__":
    main()
