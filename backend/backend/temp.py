from dataAnalysis.models import GameMetadata

query = GameMetadata.objects.all()

tournamentList = []
for gameMetadata in query:
    if not(gameMetadata.tournament in tournamentList):
        tournamentList.append(gameMetadata.tournament)

print(",".join(tournamentList))