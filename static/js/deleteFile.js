  // Eliminar imagen
  const trash = document.querySelector('.bi-trash');
  trash.addEventListener('click',()=>{
    const img = document.querySelector('.box-img img');
    // pone la  imagen por defecto
    img.src = '/static/img/profile/profile-defecto.png';
  })