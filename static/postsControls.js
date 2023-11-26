let delete_post=(postId)=>{
    let divEl=document.getElementById("postNum"+postId)
    
    const formData = new FormData();
    formData.append('postId', postId);
    

    axios.post('/deletePost', formData,{        headers: {

        'X-CSRFToken': csrftoken
    }})
      .then(function (response) {
        divEl.innerHTML=""
        
      })
      .catch(function (error) {
        console.log(error);
      });
 

}