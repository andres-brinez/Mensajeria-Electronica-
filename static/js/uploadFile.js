  // script para mostrar el nombre del archivo cargado
  const fileSelect = document.querySelector(".file-select");
  const fileElem = document.querySelector("#file");

  fileElem.addEventListener("change", (e) => {
    const fileList = e.target.files;
    fileSelect.innerHTML = fileList[0].name;
  });


/* OTRA FORMA DE HACERLO */


// var inputs = document.querySelectorAll( '.inputfile' );
// Array.prototype.forEach.call( inputs, function( input )
// {

  
// 	input.addEventListener( 'change', function( e )
// 	{
//     let label=document.querySelector( '.file-select' )
// 	  let fileName = '';

//     // si se selecciona un archivo 
// 		if( this.files && this.files.length > 1 )
// 			fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
      
		
//         // pone el nombre del archivo
// 		if( fileName )
// 			label.textContent = fileName;
// 		else
//       label.textContent = e.target.value.split( '\\' ).pop();
//     console.log(fileName) 

// 	});
// });

