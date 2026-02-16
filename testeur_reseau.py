# Testeur réseau ping des serveurs et log le resultat

import subprocess
import platform
import datetime

# fonction pour ping un serveur
def ping(host, timeout=3):
    systeme = platform.system().lower()
    
    if systeme == "windows":
        param_count = "-n"
        param_timeout = "-w"
        timeout_val = str(timeout * 1000)
    else:
        param_count = "-c"
        param_timeout = "-W"
        timeout_val = str(timeout)

    cmd = ["ping", param_count, "1", param_timeout, timeout_val, host]

    try:
        resultat = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout + 5)
        if resultat.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print("Erreur avec " + host + ": " + str(e))
        return False


# teste tous les serveurs de la liste
def tester_serveurs(serveurs):
    resultats = []
    for i in range(len(serveurs)):
        serveur = serveurs[i]
        reponse = ping(serveur)
        if reponse == True:
            status = "OK"
        else:
            status = "FAIL"
        resultats.append({"serveur": serveur, "status": status})
    return resultats


# affiche les resultats dans le terminal
def afficher_resultats(resultats):
    print("")
    print("=" * 45)
    print("       TESTEUR RESEAU - Resultats")
    print("=" * 45)
    
    for i in range(len(resultats)):
        r = resultats[i]
        if r["status"] == "OK":
            icone = "/"
        else:
            icone = "X"
        print("  " + icone + "  " + r["status"].rjust(4) + "  -  " + r["serveur"])
    
    print("=" * 45)

    ok_count = 0
    fail_count = 0
    for r in resultats:
        if r["status"] == "OK":
            ok_count = ok_count + 1
        else:
            fail_count = fail_count + 1
    
    print("  Total : " + str(ok_count) + " OK / " + str(fail_count) + " FAIL")
    print("=" * 45)
    print("")


# sauvegarde les resultats dans un fichier txt
def sauvegarder_log(resultats, fichier="reseau_log.txt"):
    maintenant = datetime.datetime.now()
    timestamp = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    
    f = open(fichier, "a", encoding="utf-8")
    f.write("\n--- Test du " + timestamp + " ---\n")
    
    for r in resultats:
        ligne = "  " + r["status"].rjust(4) + " - " + r["serveur"] + "\n"
        f.write(ligne)
    
    ok = 0
    fail = 0
    for r in resultats:
        if r["status"] == "OK":
            ok = ok + 1
        else:
            fail = fail + 1
    f.write("  Total : " + str(ok) + " OK / " + str(fail) + " FAIL\n")
    f.close()
    
    print("Resultats sauvegardes dans '" + fichier + "'")


# programme principal
def main():
    serveurs = [
        "google.com",
        "8.8.8.8",
        "1.1.1.1",
        "github.com",
        "10.0.0.5",
        "192.168.1.1",
    ]

    print("")
    print("Test en cours, veuillez patienter...")
    
    resultats = tester_serveurs(serveurs)
    afficher_resultats(resultats)
    sauvegarder_log(resultats)


if __name__ == "__main__":
    main()
