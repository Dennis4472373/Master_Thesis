Bijgevoegd zijn de completions van vier modellen: twee T5-configs en twee FLAN-T5-configs.

Parameters:
T5-base: ergens in de 200M
T5-3b: 3B
FLAN-T5-XL: 3B
FLAN-T5-XXL: 11B

FLAN-T5-XL is dus T5-3b met de extra FLAN pretraining.

Completions:
T5-base: Haalt hoge scores (tussen target en gen_comp), maar de completions liggen dus dicht bij elkaar
T5-3b: De completions zijn waardeloos. Ik heb ze bijgevoegd zodat je ze evt. kunt vergelijken met FLAN-T5-XL
FLAN-T5-XL: De completions zullen vergelijkbaar zijn met T5-base. Desondanks mogen we een hogere variatie verwacht vanwege de extra FLAN pretraining
FLAN-T5-XXL: Dit model parafraseerd en lijkt soms te hallucineren. Kijk eens op lines 8, 16, 24, 32, 62, 117 ter illustratie. 
