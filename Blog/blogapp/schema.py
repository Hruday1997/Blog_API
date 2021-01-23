from graphene_django import DjangoObjectType
from blogapp.models import Post,Comment
import graphene

#creates ObjectType for Post model
class PostType(DjangoObjectType):
    class Meta:
        model=Post

#creates ObjectType for Comment model
class CommentType(DjangoObjectType):
    class Meta:
        model=Comment

#PostInput accepts input posts from user
class PostInput(graphene.InputObjectType):
    id=graphene.ID()
    title = graphene.String()
    description = graphene.String()
    #publishDate = graphene.String()[//publish date is not required,we are generating it automatically//]
    author = graphene.String()

#CommentInput accepts input comments from user
class CommentInput(graphene.InputObjectType):
    id = graphene.ID()
    posts = graphene.List(PostInput)
    text = graphene.String()
    author = graphene.String()

#CreatePost will save the user posts in database
class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required = True)
    post = graphene.Field(PostType)

    def mutate(root, info, input=None):
        post_instance = Post(title = input.title,description = input.description,author = input.author)
        post_instance.save()
        return CreatePost(post = post_instance)

#CreateComment will save the user comments in database
class CreateComment(graphene.Mutation):
    class Arguments:
        input=CommentInput(required = True)
    comment=graphene.Field(CommentType)

    def mutate(root,info,input = None):
        Posts=[]
        for post_input in input.posts:
            post = Post.objects.get(pk = post_input['id'])
            if post is None:
                return CreateComment(comment = None)
            Posts.append(post)
        comment_instance = Comment(text = input.text,author = input.author)
        comment_instance.save()
        comment_instance.posts.set(Posts)
        return CreateComment(comment = comment_instance)

#Update the post of user in database
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        input = PostInput(required = True)
    post = graphene.Field(PostType)

    def mutate(root, info, id, input = None):
        post_instance = Post.objects.get(pk = id)
        if post_instance:
            post_instance.title = input.title
            post_instance.description = input.description
            post_instance.author = input.author
            post_instance.save()
            return UpdatePost(post = post_instance)
        return UpdatePost(post = None)

#Delete comments for the posts
class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
    comment=graphene.Field(CommentType)

    def mutate(root, info, **kwargs):
        comment_instance = Comment.objects.get(pk = kwargs['id'])
        comment_instance.delete()
        return DeleteComment(comment = None)

class Query(graphene.ObjectType):
    comment=graphene.Field(CommentType, id = graphene.Int())
    post=graphene.Field(PostType, id = graphene.Int())
    posts=graphene.List(PostType)

    def resolve_comment(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Comment.objects.get(pk = id)
        return None

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk = id)
        return None

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment= CreateComment.Field()
    update_post = UpdatePost.Field()
    delete_comment = DeleteComment.Field()


schema=graphene.Schema(query = Query, mutation = Mutation)

