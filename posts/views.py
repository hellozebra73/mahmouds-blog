from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.template import loader
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from PIL import Image
from django.conf import settings
from django.conf.urls.static import static
import boto3
import imghdr

s3_client = boto3.client("s3",aws_access_key_id="AKIAWLSAE5CQIOKI3W6L",aws_secret_access_key="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")
media_keys=["video","image"]
def posts(request):
    posts_data=list(Post.objects.all().values())
    
    for post in posts_data:
        for key in media_keys:
            if post[key]!=None:
                try:
                    s3Media = s3_client.generate_presigned_url('get_object', 
                            Params={'Bucket': "mahmouds-blog-pictures-and-videos", 'Key':post[key]},
                            ExpiresIn=200
                            )
                    post[key]=s3Media
                except:
                    post[key]=None

    template = loader.get_template('post_list.html')
    context = {'posts_data': posts_data}
    return render(request,"post_list.html", context)




    # return HttpResponse(template.render(context,request))

def create(request,id=None):
    context = {'posts_data': None}
    if id!=None:
        post_data=Post.objects.get(id=id)
        for key in media_keys:
            if post_data.__getattribute__(key)!=None:
                try:
                    s3Media = s3_client.generate_presigned_url('get_object', 
                            Params={'Bucket': "mahmouds-blog-pictures-and-videos", 'Key':post_data.__getattribute__(key)},
                            ExpiresIn=2004
                            )
                    setattr(post_data,key,s3Media)
                except:
                    setattr(post_data,key,None)

        context = {'post_data': post_data}
        
    template = loader.get_template('create_post.html')
    return render(request,'create_post.html', context)


def validate_post_data(data):
    keys=["author","title","content"]
    for key in keys:
        if not isinstance(data[key], str) or not len(data[key])>1:
            return {"correct":False,"key":key}

    return {"correct":True,"key":None}




image_types=['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']

@api_view(["POST"])
def submitPost(request):
    if request.method == 'POST':
        print("submiting....")
        author=request.data["author"]
        content=request.data["content"]
        title=request.data["title"]
        picture=request.data["picture"]
        video=request.data["video"]
        post_id=int(request.data["postId"]) if request.data["postId"].isnumeric() else None
        post_data={"author":author,"content":content,"title":title}
        validate=validate_post_data(post_data)
        
        if post_id!=None:
            old_post_data=Post.objects.get(id=post_id)
        media_names={"video":None,"image":None}
        media={"video":video,"image":picture}
        for key in media.keys():
            if  media[key]!="-1":
                if hasattr(media[key], "_name")  :
                    if post_id==None or old_post_data.__getattribute__(key)!=media[key]._name :
                        media_names[key]=media[key]._name
                        res=s3_client.put_object(Bucket = 'mahmouds-blog-pictures-and-videos', Key=media_names[key], Body=media[key])
                new_media_name=media[key]._name if hasattr(media[key], "_name") else media[key]
                if post_id!=None and old_post_data.__getattribute__(key)!=None and old_post_data.__getattribute__(key)!=new_media_name:
                    key_obj={key:old_post_data.__getattribute__(key)}
                    pm=Post.objects.filter(**key_obj)
                    if len(pm)==1:
                        s3_client.delete_object(Bucket = 'mahmouds-blog-pictures-and-videos', Key=old_post_data.__getattribute__(key))                   
                post_data[key]=media_names[key]
            else:
                post_data[key]=old_post_data.__getattribute__(key)

        if validate["correct"]:
            obj, created = Post.objects.update_or_create(id=post_id,defaults=post_data)
        data={"correct":True}
        print("done")
    return JsonResponse(data)


@api_view(["POST"])
def deletePost(request):
    if request.method == 'POST':

        post_id=int(request.data["postId"])
        old_post_data=Post.objects.get(id=post_id) 
        for key in media_keys: 
            key_obj={key:old_post_data.__getattribute__(key)}
            pm=Post.objects.filter(**key_obj)
            if len(pm)==1:
                s3_client.delete_object(Bucket = 'mahmouds-blog-pictures-and-videos', Key=old_post_data.__getattribute__(key))
        Post.objects.get(id=post_id).delete()
            
        data={"correct":True}
    return JsonResponse(data)


