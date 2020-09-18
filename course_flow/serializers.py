from rest_framework import serializers
from .models import (
    Program,
    Course,
    Preparation,
    Activity,
    Assessment,
    Artifact,
    Strategy,
    Column,
    ColumnWorkflow,
    Node,
    NodeStrategy,
    StrategyWorkflow,
    ComponentWeek,
    Component,
    Week,
    Discipline,
    Outcome,
    OutcomeNode,
    OutcomeStrategy,
    OutcomePreparation,
    OutcomeWorkflow,
    OutcomeAssessment,
    OutcomeArtifact,
    OutcomeWeek,
    NodeCompletionStatus,
    ComponentCompletionStatus,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class OutcomeSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Outcome
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "hash",
            "author",
        ]

    def create(self, validated_data):
        return Outcome.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.save()
        return instance


class OutcomeNodeSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer(allow_null=True)

    class Meta:
        model = OutcomeNode
        fields = ["node", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ParentNodeSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Node
        fields = [
            "id",
            "title",
            "description",
            "last_modified",
            "hash",
            "author",
            "work_classification",
            "activity_classification",
            "classification",
        ]


class ParentStrategySerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Strategy
        fields = [
            "id",
            "title",
            "description",
            "last_modified",
            "hash",
            "author",
        ]


class NodeSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomenode_set = serializers.SerializerMethodField()

    parent_node = ParentNodeSerializer(allow_null=True)

    class Meta:
        model = Node
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "column",
            "hash",
            "author",
            "work_classification",
            "activity_classification",
            "classification",
            "outcomenode_set",
            "is_original",
            "parent_node",
        ]

    def get_outcomenode_set(self, instance):
        links = instance.outcomenode_set.all().order_by("rank")
        return OutcomeNodeSerializer(links, many=True).data

    def create(self, validated_data):
        return Node.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.classification = validated_data.get(
            "classification", instance.classification
        )
        instance.work_classification = validated_data.get(
            "work_classification", instance.work_classification
        )
        instance.activity_classification = validated_data.get(
            "activity_classification", instance.activity_classification
        )
        for outcomenode_data in self.initial_data.pop("outcomenode_set"):
            outcomenode_serializer = OutcomeNodeSerializer(
                OutcomeNode.objects.get(id=outcomenode_data["id"]),
                data=outcomenode_data,
            )
            outcomenode_serializer.is_valid()
            outcomenode_serializer.save()
        instance.save()
        return instance


class NodeStrategySerializer(serializers.ModelSerializer):

    node = NodeSerializer()

    class Meta:
        model = NodeStrategy
        fields = ["strategy", "node", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data["rank"]
        node_data = self.initial_data.pop("node")
        node_serializer = NodeSerializer(
            Node.objects.get(id=node_data["id"]), node_data
        )
        node_serializer.is_valid()
        node_serializer.save()
        instance.save()
        return instance


class OutcomeStrategySerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeStrategy
        fields = ["strategy", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ColumnSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Column
        fields = ["id", "title", "author", "created_on", "last_modified"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance

    def create(self, validated_data):
        return Column.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )


class StrategySerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    nodestrategy_set = serializers.SerializerMethodField()

    outcomestrategy_set = serializers.SerializerMethodField()

    parent_strategy = ParentStrategySerializer(allow_null=True)

    num_children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Strategy
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "hash",
            "default",
            "author",
            "nodestrategy_set",
            "outcomestrategy_set",
            "is_original",
            "parent_strategy",
            "num_children",
        ]

    def get_num_children(self, instance):
        return instance.strategy_set.count()

    def get_nodestrategy_set(self, instance):
        links = instance.nodestrategy_set.all().order_by("rank")
        return NodeStrategySerializer(links, many=True).data

    def get_outcomestrategy_set(self, instance):
        links = instance.outcomestrategy_set.all().order_by("rank")
        return OutcomeStrategySerializer(links, many=True).data

    def create(self, validated_data):
        return Strategy.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for nodestrategy_data in self.initial_data.pop("nodestrategy_set"):
            nodestrategy_serializer = NodeStrategySerializer(
                NodeStrategy.objects.get(id=nodestrategy_data["id"]),
                data=nodestrategy_data,
            )
            nodestrategy_serializer.is_valid()
            nodestrategy_serializer.save()
        for outcomestrategy_data in self.initial_data.pop(
            "outcomestrategy_set"
        ):
            outcomestrategy_serializer = OutcomeStrategySerializer(
                OutcomeStrategy.objects.get(id=outcomestrategy_data["id"]),
                data=outcomestrategy_data,
            )
            outcomestrategy_serializer.is_valid()
            outcomestrategy_serializer.save()
        instance.save()
        return instance


class StrategyWorkflowSerializer(serializers.ModelSerializer):

    strategy = StrategySerializer()

    class Meta:
        model = StrategyWorkflow
        fields = ["workflow", "strategy", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.rank)
        strategy_data = self.initial_data.pop("strategy")
        strategy_serializer = StrategySerializer(
            Strategy.objects.get(id=strategy_data["id"]), strategy_data
        )
        if strategy_serializer.is_valid():
            strategy_serializer.save()
        instance.save()
        return instance


class ColumnWorkflowSerializer(serializers.ModelSerializer):
    column = ColumnSerializer()

    class Meta:
        model = ColumnWorkflow
        fields = ["workflow", "column", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.rank)
        column_data = self.initial_data.pop("column")
        column_serializer = ColumnSerializer(
            Column.objects.get(id=column_data["id"]), column_data
        )
        if column_serializer.is_valid():
            column_serializer.save()
        instance.save()
        return instance


class OutcomeWorkflowSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeWorkflow
        fields = ["workflow", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.rank)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    strategyworkflow_set = serializers.SerializerMethodField()

    columnworkflow_set = serializers.SerializerMethodField()

    outcomeworkflow_set = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "columnworkflow_set",
            "strategyworkflow_set",
            "outcomeworkflow_set",
            "is_original",
            "parent_activity",
        ]

    def get_columnworkflow_set(self, instance):
        links = instance.columnworkflow_set.all().order_by("rank")
        return ColumnWorkflowSerializer(links, many=True).data

    def get_strategyworkflow_set(self, instance):
        links = instance.strategyworkflow_set.all().order_by("rank")
        return StrategyWorkflowSerializer(links, many=True).data

    def get_outcomeworkflow_set(self, instance):
        links = instance.outcomeworkflow_set.all().order_by("rank")
        return OutcomeWorkflowSerializer(links, many=True).data

    def create(self, validated_data):
        if User.objects.filter(username=self.initial_data["author"]).exists():
            author = User.objects.get(username=self.initial_data["author"])
        else:
            author = None
        activity = Activity.objects.create(author=author, **validated_data)

        """
        do not update the following code, this will only be used for default strategy creation
        """
        if "strategyactivity_set" in self.initial_data.keys():
            Strategy.objects.filter(default=True).update(default=False)
            for strategyactivity_data in self.initial_data.pop(
                "strategyactivity_set"
            ):
                strategy_data = strategyactivity_data.pop("strategy")
                null_author = strategy_data.pop("author")
                nodestrategy_set = strategy_data.pop("nodestrategy_set")
                outcomestategy_set = strategy_data.pop("outcomestrategy_set")
                strategy = Strategy.objects.create(
                    author=author, **strategy_data
                )
                link = StrategyActivity.objects.create(
                    strategy=strategy,
                    activity=activity,
                    rank=strategyactivity_data["rank"],
                )
                for nodestrategy_data in nodestrategy_set:
                    node_data = nodestrategy_data.pop("node")
                    null_author = node_data.pop("author")
                    outcomenode_set = node_data.pop("outcomenode_set")
                    node = Node.objects.create(author=author, **node_data)
                    link = NodeStrategy.objects.create(
                        node=node,
                        strategy=strategy,
                        rank=nodestrategy_data["rank"],
                    )
        return activity

    def update(self, instance, validated_data):

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for strategyworkflow_data in self.initial_data.pop(
            "strategyworkflow_set"
        ):
            strategyworkflow_serializer = StrategyWorkflowSerializer(
                StrategyWorkflow.objects.get(id=strategyworkflow_data["id"]),
                data=strategyworkflow_data,
            )
            strategyworkflow_serializer.is_valid()
            strategyworkflow_serializer.save()
        for outcomeworkflow_data in self.initial_data.pop(
            "outcomeworkflow_set"
        ):
            outcomeworkflow_serializer = OutcomeWorkflowSerializer(
                OutcomeWorkflow.objects.get(id=outcomeworkflow_data["id"]),
                data=outcomeworkflow_data,
            )
            outcomeworkflow_serializer.is_valid()
            outcomeworkflow_serializer.save()
        for columnworkflow_data in self.initial_data.pop("columnworkflow_set"):
            columnworkflow_serializer = ColumnWorkflowSerializer(
                ColumnWorkflow.objects.get(id=columnworkflow_data["id"]),
                data=columnworkflow_data,
            )
            columnworkflow_serializer.is_valid()
            columnworkflow_serializer.save()
        instance.save()
        return instance


class OutcomePreparationSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomePreparation
        fields = ["preparation", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class PreparationSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomepreparation_set = serializers.SerializerMethodField()

    class Meta:
        model = Preparation
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomepreparation_set",
            "is_original",
            "parent_preparation",
        ]

    def get_outcomepreparation_set(self, instance):
        links = instance.outcomepreparation_set.all().order_by("rank")
        return OutcomePreparationSerializer(links, many=True).data

    def create(self, validated_data):
        return Preparation.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for outcomepreparation_data in self.initial_data.pop(
            "outcomepreparation_set"
        ):
            outcomepreparation_serializer = OutcomePreparationSerializer(
                OutcomePreparation.objects.get(
                    id=outcomepreparation_data["id"]
                ),
                data=outcomepreparation_data,
            )
            outcomepreparation_serializer.is_valid()
            outcomepreparation_serializer.save()
        instance.save()
        return instance


class OutcomeAssessmentSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeAssessment
        fields = ["assessment", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class AssessmentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomeassessment_set = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomeassessment_set",
            "is_original",
            "parent_assessment",
        ]

    def get_outcomeassessment_set(self, instance):
        links = instance.outcomeassessment_set.all().order_by("rank")
        return OutcomeAssessmentSerializer(links, many=True).data

    def create(self, validated_data):
        return Assessment.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for outcomeassessment_data in self.initial_data.pop(
            "outcomeassessment_set"
        ):
            outcomeassessment_serializer = OutcomeAssessmentSerializer(
                OutcomeAssessment.objects.get(id=outcomeassessment_data["id"]),
                data=outcomeassessment_data,
            )
            outcomeassessment_serializer.is_valid()
            outcomeassessment_serializer.save()
        instance.save()
        return instance


class OutcomeArtifactSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeArtifact
        fields = ["artifact", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ArtifactSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomeartifact_set = serializers.SerializerMethodField()

    class Meta:
        model = Artifact
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomeartifact_set",
            "is_original",
            "parent_artifact",
        ]

    def get_outcomeartifact_set(self, instance):
        links = instance.outcomeartifact_set.all().order_by("rank")
        return OutcomeArtifactSerializer(links, many=True).data

    def create(self, validated_data):
        return Artifact.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for outcomeartifact_data in self.initial_data.pop(
            "outcomeartifact_set"
        ):
            outcomeartifact_serializer = OutcomeArtifactSerializer(
                OutcomeArtifact.objects.get(id=outcomeartifact_data["id"]),
                data=outcomeartifact_data,
            )
            outcomeartifact_serializer.is_valid()
            outcomeartifact_serializer.save()
        instance.save()
        return instance


class WeekLevelComponentSerializer(serializers.ModelSerializer):

    content_object = serializers.SerializerMethodField()

    content_type = serializers.SerializerMethodField()

    content_type_in_text = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = [
            "content_object",
            "content_type",
            "content_type_in_text",
            "id",
        ]

    def get_content_object(self, instance):
        if type(instance.content_object) == Activity:
            return ActivitySerializer(instance.content_object).data
        elif type(instance.content_object) == Preparation:
            return PreparationSerializer(instance.content_object).data
        elif type(instance.content_object) == Assessment:
            return AssessmentSerializer(instance.content_object).data
        else:
            return ArtifactSerializer(instance.content_object).data

    def get_content_type(self, instance):
        if type(instance.content_object) == Activity:
            return 0
        elif type(instance.content_object) == Preparation:
            return 1
        elif type(instance.content_object) == Assessment:
            return 2
        else:
            return 3

    def get_content_type_in_text(self, instance):
        if type(instance.content_object) == Activity:
            return "activity"
        elif type(instance.content_object) == Preparation:
            return "preparation"
        elif type(instance.content_object) == Assessment:
            return "assessment"
        else:
            return "artifact"

    def update(self, instance, validated_data):
        content_object_data = self.initial_data.pop("content_object")
        if type(instance.content_object) == Activity:
            content_object_serializer = ActivitySerializer(
                Activity.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        elif type(instance.content_object) == Preparation:
            content_object_serializer = PreparationSerializer(
                Preparation.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        elif type(instance.content_object) == Assessment:
            content_object_serializer = AssessmentSerializer(
                Assessment.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        else:
            content_object_serializer = ArtifactSerializer(
                Artifact.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        content_object_serializer.is_valid()
        content_object_serializer.save()
        instance.save()
        return instance


class ComponentWeekSerializer(serializers.ModelSerializer):

    component = WeekLevelComponentSerializer()

    class Meta:
        model = ComponentWeek
        fields = ["week", "component", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.rank)
        component_data = self.initial_data.pop("component")
        component_serializer = WeekLevelComponentSerializer(
            Component.objects.get(id=component_data["id"]), component_data
        )
        component_serializer.is_valid()
        component_serializer.save()
        instance.save()
        return instance


class OutcomeWeekSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeWeek
        fields = ["week", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get("rank", instance.title)
        outcome_data = self.initial_data.pop("outcome")
        outcome_serializer = OutcomeSerializer(
            Outcome.objects.get(id=outcome_data["id"]), outcome_data
        )
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class WeekSerializer(serializers.ModelSerializer):

    componentweek_set = serializers.SerializerMethodField()

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomeweek_set = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = [
            "id",
            "title",
            "hash",
            "created_on",
            "last_modified",
            "author",
            "componentweek_set",
            "outcomeweek_set",
        ]

    def get_componentweek_set(self, instance):
        links = instance.componentweek_set.all().order_by("rank")
        return ComponentWeekSerializer(links, many=True).data

    def get_outcomeweek_set(self, instance):
        links = instance.outcomeweek_set.all().order_by("rank")
        return OutcomeWeekSerializer(links, many=True).data

    def create(self, validated_data):
        return Week.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        for componentweek_data in self.initial_data.pop("componentweek_set"):
            componentweek_serializer = ComponentWeekSerializer(
                ComponentWeek.objects.get(id=componentweek_data["id"]),
                data=componentweek_data,
            )
            componentweek_serializer.is_valid()
            componentweek_serializer.save()
        for outcomeweek_data in self.initial_data.pop("outcomeweek_set"):
            outcomeweek_serializer = OutcomeWeekSerializer(
                OutcomeWeek.objects.get(id=outcomeweek_data["id"]),
                data=outcomeweek_data,
            )
            outcomeweek_serializer.is_valid()
            outcomeweek_serializer.save()
        instance.save()
        return instance


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "title"]


class CourseSerializer(serializers.ModelSerializer):

    strategyworkflow_set = serializers.SerializerMethodField()
    
    columnworkflow_set = serializers.SerializerMethodField()

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    discipline = DisciplineSerializer(read_only=True)

    outcomeworkflow_set = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "strategyworkflow_set",
            "outcomeworkflow_set",
            "columnworkflow_set",
            "discipline",
            "is_original",
            "parent_activity",
        ]

    def get_strategyworkflow_set(self, instance):
        links = instance.strategyworkflow_set.all().order_by("rank")
        return StrategyWorkflowSerializer(links, many=True).data
    
    def get_columnworkflow_set(self, instance):
        links = instance.columnworkflow_set.all().order_by("rank")
        return ColumnWorkflowSerializer(links, many=True).data

    def get_outcomeworkflow_set(self, instance):
        links = instance.outcomeworkflow_set.all().order_by("rank")
        return OutcomeWorkflowSerializer(links, many=True).data

    def create(self, validated_data):
        return Course.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for strategyworkflow_data in self.initial_data.pop("strategyworkflow_set"):
            strategyworkflow_serializer = StrategyWorkflowSerializer(
                StrategyWorkflow.objects.get(id=strategyworkflow_data["id"]),
                data=strategyworkflow_data,
            )
            strategyworkflow_serializer.is_valid()
            strategyworkflow_serializer.save()
        for columnworkflow_data in self.initial_data.pop("columnworkflow_set"):
            columnworkflow_serializer = ColumnWorkflowSerializer(
                ColumnWorkflow.objects.get(id=columnworkflow_data["id"]),
                data=columnworkflow_data,
            )
            columnworkflow_serializer.is_valid()
            columnworkflow_serializer.save()
        for outcomeworkflow_data in self.initial_data.pop("outcomeworkflow_set"):
            outcomeworkflow_serializer = OutcomeWorkflowSerializer(
                OutcomeWorkflow.objects.get(id=outcomeworkflow_data["id"]),
                data=outcomeworkflow_data,
            )
            outcomeworkflow_serializer.is_valid()
            outcomeworkflow_serializer.save()
        instance.save()
        return instance


class ProgramLevelComponentSerializer(serializers.ModelSerializer):

    content_object = serializers.SerializerMethodField()

    content_type = serializers.SerializerMethodField()

    content_type_in_text = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = [
            "content_object",
            "content_type",
            "content_type_in_text",
            "id",
        ]

    def get_content_object(self, instance):
        if type(instance.content_object) == Course:
            return CourseSerializer(instance.content_object).data
        else:
            return AssessmentSerializer(instance.content_object).data

    def get_content_type(self, instance):
        if type(instance.content_object) == Course:
            return 0
        else:
            return 1

    def get_content_type_in_text(self, instance):
        if type(instance.content_object) == Course:
            return "course"
        else:
            return "assessment"

    def update(self, instance, validated_data):
        content_object_data = self.initial_data.pop("content_object")
        if type(instance.content_object) == Course:
            content_object_serializer = CourseSerializer(
                Course.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        else:
            content_object_serializer = AssessmentSerializer(
                Assessment.objects.get(id=content_object_data["id"]),
                data=content_object_data,
            )
        content_object_serializer.is_valid()
        content_object_serializer.save()
        instance.save()
        return instance


class ProgramSerializer(serializers.ModelSerializer):

    strategyworkflow_set = serializers.SerializerMethodField()

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    outcomeworkflow_set = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "strategyworkflow_set",
            "outcomeworkflow_set",
        ]

    def get_strategyworkflow_set(self, instance):
        links = instance.strategyworkflow_set.all().order_by("rank")
        return StrategyWorkflowSerializer(links, many=True).data

    def get_outcomeworkflow_set(self, instance):
        links = instance.outcomeworkflow_set.all().order_by("rank")
        return OutcomeWorkflowSerializer(links, many=True).data

    def create(self, validated_data):
        return Program.objects.create(
            author=User.objects.get(username=self.initial_data["author"]),
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        for strategyworkflow_data in self.initial_data.pop("strategyworkflow_set"):
            strategyworkflow_serializer = StrategyWorkflowSerializer(
                StrategyWorkflow.objects.get(id=strategyworkflow_data["id"]),
                data=strategyworkflow_data,
            )
            strategyworkflow_serializer.is_valid()
            strategyworkflow_serializer.save()
        for outcomeworkflow_data in self.initial_data.pop("outcomeworkflow_set"):
            outcomeworkflow_serializer = OutcomeWorkflowSerializer(
                OutcomeWorkflow.objects.get(id=outcomeworkflow_data["id"]),
                data=outcomeworkflow_data,
            )
            outcomeworkflow_serializer.is_valid()
            outcomeworkflow_serializer.save()
        instance.save()
        return instance


serializer_lookups = {
    "node": NodeSerializer,
    "strategy": StrategySerializer,
    "column": ColumnSerializer,
    "activity": ActivitySerializer,
    "assessment": AssessmentSerializer,
    "preparation": PreparationSerializer,
    "artifact": ArtifactSerializer,
    "week": WeekSerializer,
    "course": CourseSerializer,
    "program": ProgramSerializer,
}
