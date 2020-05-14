import random

DEFAULT = [
    "(J'ai un gros problème de générateur)",
    "(Je ne sais pas quelle phrase générer)",
    "(Je crois que mon générateur me lâche, ce sera notre petit secret.)",
]

CATALOG = {
    "computing.channel": [
        "Je suis toujours en train de compter les concombres de {}. Déso.",
        "Encore en train de compte le channel. Je fais au mieux.",
        "Je parcours toujours l'historique de ce channel en quête d'un max de concombres.",
    ],
    "computing.global": [
        "Je compte toujours là, je veux pas donner d'informations erronnées.",
        "Encore en train de compter !",
        "J'arrive, j'arrive. J'ai presque fini de compter les concombres.",
    ],
    "stats.global.intro": [
        "Le top du top :",
        "Mes stars. Je le pense vraiment :",
        "J'aurais parié sur le 3. Comme quoi :",
        "Quelle aventure mes amis :",
    ],
    "stats.channel.intro": [
        "Les kings et queens du channel {} :",
        "Le classement de {} :",
        "La crème de {} :",
        "Les stats de {} ? Bien sûr les voici :",
    ],
    "unknown.intro": [
        "En toute transparence je ne comprends pas cette commande.",
        "Mmmh je ne suis pas sûr de pouvoir faire quoi que ce soit avec ça.",
        "Je ne sais pas qui t'a donné cette commande mais ce n'est pas quelqu'un de confiance.",
        "Ok on se calme et on arrête les propos incohérents.",
        "Alors là je ne m'attendais pas à ça.",
        "Rien compris.",
        "*{}* ? Sérieusement ?",
        "Ok reprenons tout depuis le début.",
    ],
    "unknown.help": [
        "Essaie {} pour voir.",
        "Peut-être que {} pourrait t'aider.",
        "{} est très certainement un bon point de départ.",
        "Répète après moi : {}",
    ],
}


class ResponseGenerator:
    def generate(self, key):
        return random.choice(CATALOG.get(key, DEFAULT))
