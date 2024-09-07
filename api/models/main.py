from neomodel import (
    config,
    db,
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    RelationshipTo,
    StructuredRel,
    DateTimeProperty,
    BooleanProperty,
    FloatProperty,
    ArrayProperty,
)


class FromRel(StructuredRel):
    pass


class Reaction(StructuredRel):
    type = StringProperty(required=True)


class User(StructuredNode):
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    name = StringProperty(max_length=50, required=True)
    email = StringProperty(unique_index=True, required=True)
    password = StringProperty(max_length=50, required=True)
    is_available = BooleanProperty(default=True)
    activity = FloatProperty(default=0.0)
    latest_login = DateTimeProperty(default_now=True)
    introduction = StringProperty(max_length=500, default="")
    profile_image = StringProperty(default="")
    background_image = StringProperty(default="")
    posted = RelationshipTo("Post", "POSTED", model=FromRel)
    following = RelationshipTo("User", "FOLLOWING", model=FromRel)
    block = RelationshipTo("User", "BLOCK", model=FromRel)
    reaction = RelationshipTo("Post" or "Comment", "REACTION", model=Reaction)
    hosted = RelationshipTo("Recruitment", "HOSTED", model=FromRel)
    commented = RelationshipTo("Comment", "COMMENTED", model=FromRel)
    applied = RelationshipTo("Recruitment", "APPLIED", model=FromRel)


class Post(StructuredNode):
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    content = StringProperty(max_length=500, required=True)
    image_urls = ArrayProperty(StringProperty())


class Recruitment(StructuredNode):
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    title = StringProperty(max_length=50, required=True)
    description = StringProperty(max_length=500, required=True)
    image_urls = ArrayProperty(StringProperty())
    deadline = DateTimeProperty()


class Comment(StructuredNode):
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    content = StringProperty(max_length=500, required=True)
    image_urls = ArrayProperty(StringProperty())
    post = RelationshipTo(Post, "COMMENTED", model=FromRel)
    reply = RelationshipTo("Comment", "REPLY", model=FromRel)


# jim = Person(name="Jim", age=3).save()  # Create
# jim.age = 4
# jim.save()  # Update, (with validation)
# jim.delete()
# jim = Person(name="Jim", age=3).save()
# jim.refresh()  # reload properties from the database
# id = jim.element_id  # neo4j internal element id

# # Return all nodes
# all_nodes = Person.nodes.all()

# # Returns Person by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
# query = f"MATCH (n) WHERE elementId(n) = '{id}' RETURN n"
# results, meta = db.cypher_query(query)

# # Returns Person list by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
# jim = Person.nodes.filter(name="Jim")

# # Will return None unless "bob" exists
# someone = Person.nodes.get_or_none(name="bob")

# # Will return the first Person node with the name bob. This raises neomodel.DoesNotExist if there's no match.
# someone = Person.nodes.first(name="Jim")

# # Will return the first Person node with the name bob or None if there's no match
# someone = Person.nodes.first_or_none(name="bob")

# # Return set of nodes
# people = Person.nodes.filter(age__gt=3)

# germany = Country(code="DE").save()
# jim = Person(name="Jim", age=3).save()
# jim.country.connect(germany)
# berlin = City(name="Berlin").save()
# berlin.country.connect(germany)
# jim.city.connect(berlin)
# germany.inhabitant.connect(jim)

# if jim.country.is_connected(germany):
#     print("Jim's from Germany")

# for p in germany.inhabitant.all():
#     print(p.name)  # Jim

# len(germany.inhabitant)  # 1

# # Find people called 'Jim' in germany
# # germany.inhabitant.search(name="Jim") 使えない

# # Find all the people called in germany except 'Jim'
# germany.inhabitant.exclude(name="Jim")

# # Remove Jim's country relationship with Germany
# jim.country.disconnect(germany)

# usa = Country(code="US").save()
# jim.country.connect(usa)
# jim.country.connect(germany)

# # Remove all of Jim's country relationships
# jim.country.disconnect_all()

# jim.country.connect(usa)
# # Replace Jim's country relationship with a new one
# jim.country.replace(germany)

# # The following call will generate one MATCH with traversal per
# # item in .fetch_relations() call
# results = Person.nodes.fetch_relations("country").all()
# for result in results:
#     print(result[0])  # Person
#     print(result[1])  # associated Country

# # Go from person to City then Country
# Person.nodes.fetch_relations("city__country").all()
