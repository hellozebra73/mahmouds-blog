
let onSubmit=()=>{
    let postId=document.getElementById("postId").innerHTML;
    let author=document.getElementById("author").value;
    let title=document.getElementById("titleInput").value;
    let content=document.getElementById("content").value;
    let picture= document.getElementById("pictureUpload").files[0]
    let video= document.getElementById("videoUpload").files[0]
    let submitButton=document.getElementById("submitButton");
    submitButton.innerHTML="Saving..."

    if(document.getElementById("output").src && picture==undefined && document.getElementById("output").src.slice(-4)!="null"){
      picture=-1
    }
    if(document.getElementById("videoElement")?.firstChild?.src && video==undefined &&document.getElementById("videoElement").firstChild.src.slice(-4)!="null"){
     
      video=-1
    }
    const formData = new FormData();
    formData.append('postId', postId);
    formData.append('picture', picture);
    formData.append('author', author);
    formData.append('title', title);
    formData.append('content', content);
    formData.append('picture', picture);
    formData.append('video', video);


    axios.post('/submit', formData,{        headers: {

        'X-CSRFToken': csrftoken
    }})
      .then(function (response) {
        submitButton.innerHTML="Submit"
        document.getElementById("postSaved").style.diplay="block";
        document.getElementById("postSaved").innerHTML="Post Saved! X"
      })
      .catch(function (error) {
        console.log(error);
      });
 
}


let closePostSaved=()=>{
  document.getElementById("postSaved").innerHTML="";
}



function changeBG(buttonId,divId,mediaId,fileType) {
 
  let inputButton = document.getElementById(buttonId)
    var file = inputButton.files[0];
    if (file!=undefined){
    if(file && file['type'].split('/')[0] === fileType){
        let diplayDiv=document.getElementById(divId);
        diplayDiv.style.display="block";
        var mediaElement = document.getElementById(mediaId);
        switch(fileType){
        case "image":
          mediaElement.src = URL.createObjectURL(file);
          mediaElement.style.width="15vw"
          break
        case "video":
          if(mediaElement.firstChild!=null){
            diplayDiv.removeChild(diplayDiv.firstChild)
            let new_video = document.createElement('video');
            new_video.setAttribute('id', "videoElement");
            new_video.setAttribute('width', 320);
            new_video.setAttribute('height', 240);
            new_video.setAttribute('controls',true);
            diplayDiv.appendChild(new_video)
            mediaElement=new_video;

          }
        
          
          var source = document.createElement('source');
          source.setAttribute('src', URL.createObjectURL(file));
          mediaElement.appendChild(source)
        
      }
        


    }
    else{
      inputButton.value=null;
      inputButton.label=""
      var mediaElement = document.getElementById(mediaId);
      mediaElement.src ="";
      mediaElement.removeChild(mediaElement.firstChild);
    }
  }
}


let removeMedia=(buttonId,divId,mediaId)=>{
  let inputButton= document.getElementById(buttonId)
  inputButton.value=null
  let diplayPicture=document.getElementById(divId)
  diplayPicture.style.display="none"
  var output = document.getElementById(mediaId);
  output.src =null;
  if(output.firstChild!=null){
    output.firstChild.src=null
  }


  
}

