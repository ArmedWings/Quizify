from PySide6.QtCore import QEvent


def get_path():
    config_path = "config.txt"
    try:
        with open(config_path, "r") as config_file:
            for line in config_file:
                if line.startswith("catalog="):
                    folder_path = line.split("catalog=")[1].strip()
                    return folder_path
    except FileNotFoundError:
        print("Файл конфигурации не найден")
        return None

def score_scaled(score1, score2):
    score = (score1/score2)*100
    if score < 50:
        return 2
    elif score < 75:
        return 3
    elif score < 95:
        return 4
    else:
        return 5


def set_style_scaled(element, score):
    score = score.split("/")
    myscore = score_scaled(int(score[0]), int(score[1]))
    if myscore == 2:
        element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FF0000;")
    elif myscore == 3:
        element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FF7F00;")
    elif myscore == 4:
        element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FFFF00;")
    elif myscore == 5:
        element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #00FF00;")
def hovered_style_scaled(element, score, event):
    score = score.split("/")
    myscore = score_scaled(int(score[0]), int(score[1]))

    if event.type() == QEvent.Enter:
        if myscore == 2:
            element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FF0000;")
        elif myscore == 3:
            element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FF7F00;")
        elif myscore == 4:
            element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #FFFF00;")
        elif myscore == 5:
            element.setStyleSheet("font-size: 14pt; background-color: #111111; border: 1px solid #00FF00;")
    elif event.type() == QEvent.Leave:
        if myscore == 2:
            element.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #FF0000;")
        elif myscore == 3:
            element.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #FF7F00;")
        elif myscore == 4:
            element.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #FFFF00;")
        elif myscore == 5:
            element.setStyleSheet("font-size: 14pt; background-color: #191919; border: 1px solid #00FF00;")



