// saber la url
const url = window.location.href;

// saber si el id contiene el mensaje
if (url.includes('delete')) {
    

    if  (url.includes('true')){
        Swal.fire(
            'Eliminado!',
            'El mensaje se eliminó correctamente.',
            'success'
        )
        

    }

       
    else{
        Swal.fire(
            'Error!',
            'El mensaje no se pudo eliminar.',
            'error'
        )
    }
    
    
}

else if (url.includes('edit')) {
    if (url.includes('true'))
        Swal.fire(
            'Editado!',
            'El mensaje se editó correctamente.',
            'success'
        )
        
    else
        Swal.fire(
            'Error!',
            'El mensaje no se pudo editar.',
            'error'
        )

    // esperar un tiempo
    
}


