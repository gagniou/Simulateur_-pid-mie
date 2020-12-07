# Simulateur_epidemie
un simulateur simple d'épidémie comprenant divers facteurs tels que la vaccination, l'augmentation de la population concernés, le taux de décés et le taux de contagion 


la pandémie actuelle rend intéressant le fait d'essayer de simuler une épridémie et la compréhension du système de vague dont on entend parler ainsi les paramètre initiaux de la simulation sont fait pour permettre un sytème de vague facile.

Fonctionement de la simulation:
le principe de base est simple, la simulation focntionne par round, a chaque round chaque bloc doit se rendre depuis sa case initiale a une nouvelle case, a la fin de chaque round chaque bloc a une chance de tomber malade si il est dans la même case qu'un bloc malade, les chance sont multipliée si il est en présence de plusieurs blocs malades. les blocs malades ont une chance de mourir dépendante du taux de décés de la maladie, et aprés un certains nombres de round ils guériront

données importantes:
-Number : correspond au nombre de bloc total 
-Recovery : nombre de round necessaire pour guérir de la maladie ( passage du rouge ou blanc)
-Imunity : nombre de jour pendant lequels un bloc ne peut as retomber malade ( blocs blanc repasse bleu apres ce délai)

- R : taux de contagion chance qu'aura un bloc de tomber malade lorsqu'il sera en présence d'un bloc malade
(par rapport a un R d'une épidémie on peut donc le retrouver en effectuant le calcul suivant )
nombre de bloc sains * R / nombre de case (64) 
on a donc avec les stats de déart un R de 2000*0.025/64 : 0.78
mais notre R évolu en permanence avec la quantité de personne immunisé ou vacciné qui sont a retirer de l'équation

-D :  le taux de déces , probabilité qu'a un bloc de mourir si il est malade a la fin d'un round

-V : la chance de vaccination, quelle probabilité un bloc sain a de se faire vacciner a chaque round


les modifications a venir:
-passer d'une chance de vaccination a un taux moyen de vacciné dans la population
-proposer un R plus réel et intuitif (via l'équation présenté ci dessus )
-une option pour réguler l'augmentation de la population
