import re
import sys

from get_data import get_data

if __name__ == "__main__":
    # needs manual setup because the cri doesn't have an api to get groups
    students: list[str] = ["adam.mcibah", "ahash.likitharan", "ahmed.mezghani", "alex.debelli-gonin",
                           "alexis.kouvoua-fouka",
                           "baptiste.ducruy", "carol.legout-sales", "clement.raulo", "davy.beninos", "enzo.dugas",
                           "farah.tab",
                           "ghali.aboulal", "hong-cheng.taing", "ikram.heroual", "ilian.ben-senouci", "jacques.jiao",
                           "joachim.joron",
                           "julie.domrane", "kilen.millot", "lehen.taranne", "levana.zran", "loic.rabetrano",
                           "marc-shadrack.bumsong-bell", "maxence.gouvaert-de-jesus", "milena.dziekan",
                           "mohamed-aziz.el-guares",
                           "mohamed-djibril.touil", "mohamed-rayan.belkacemi", "nada.habbane", "nathanael.isla-y-ortiz",
                           "noam.assouline", "omar.seif", "quentin.martinet", "robin.menoux", "samuel.huang",
                           "shadanaa.sivaraja",
                           "theo.egea", "theo.laradji", "timeo.borghesi", "victor.rousseau", "yoann.papadacci"]

    # Comment this line once done
    print("This needs a manual setup for students: edit the ClassResult/__main__.py file's students variable according to your students.")
    regex = re.compile("prog-[0-9]0[0-9]-[pe]-[0-9]{2}-[0-9]{4}")
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print("Usage: ClassResult <activity>")
        print(f"\tactivity being the activity code with regex: {regex.pattern}")
        print(f"\texample: ClassResult prog-101-02-p-2031 for the 2nd practicals of the 2031's first year and first bimester")
        sys.exit(1)

    activity = sys.argv[1]

    if not regex.match(activity):
        print(f"Activity name does not obey regular expression: {regex.pattern}")
        sys.exit(1)

    get_data(sys.argv[1], students)
