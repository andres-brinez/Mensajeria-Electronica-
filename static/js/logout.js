// mensaje de confirmación de cerrar sesión

const  button = document.getElementById('logout')
    button.addEventListener('click', () => {
        Swal.fire({
            title: '¿Está seguro?',
            text: "¿Desea cerrar sesión?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, cerrar sesión'
            })
            .then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/login'
                }
        })
    })