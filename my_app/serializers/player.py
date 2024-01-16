from rest_framework import serializers 

from .player_skill import PlayerSkillSerializer
from ..models.player import Player
from ..models.player_skill import PlayerSkill

class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']

    def create(self, validated_data):
        var = validated_data.pop("playerSkills")
        playerSkills = []
        if (type(var) == dict):
            playerSkills.append(var)
        else:
            for i in var:
                playerSkills.append(i)

        player = Player.objects.create(**validated_data)
        for playerSkill in playerSkills:
            # playerID is our foreign key
            PlayerSkill.objects.create(**playerSkill, player=player)
        return player

    def update(self, instance, validated_data):
        var = validated_data.pop("playerSkills")
        playerSkills = []
        if (type(var) == dict):
            playerSkills.append(var)
        else:
            for i in var:
                playerSkills.append(i)

        # if we do not pass a name we just put the instance.name
        instance.name = validated_data.get("name", instance.name)
        instance.position = validated_data.get("position", instance.position)
        instance.save()

        existing_skills = [i.skill for i in instance.playerSkills.all()]
        for playerSkill in playerSkills:
            if playerSkill["skill"] in existing_skills:  # we are updating the skill
                var = PlayerSkill.objects.get(skill=playerSkill["skill"], player=instance)
                var.value = playerSkill.get("value", var.value)
                var.save()
            else:
                PlayerSkill.objects.create(**playerSkill, player=instance)

        return instance