from django.db import models


class BehaviorModelsMetadata(models.Model):
    uuid = models.UUIDField("uuid", max_length=240)
    modelType = models.CharField("model_type", max_length=240)
    modelName = models.CharField("model_name", max_length=240)
    role = models.CharField("role", max_length=240)
    kmo = models.FloatField("kmo")
    tournamentDict = models.CharField("tournament_dict", max_length=1000)
    nbFactors = models.IntegerField("nbFactors")
    factorsName = models.CharField("factorsName", max_length=1000)
    selected = models.BooleanField("selected")

    def __str__(self) -> str:
        return "uuid:" + str(self.uuid) + ", role:" + self.role + ", kmo:" + str(self.kmo)


