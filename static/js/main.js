$(document).ready( function () {
    //Table
    var table = $('#dataTable').DataTable( {
        responsive: true,
        columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            defaultContent: "",
            targets:   [0],
        } ],
        "dom": '<"top"lrpft><"bottom"tip>',
        select: {
            style:    'multi',
            selector: 'td:first-child',
        },
        order: [[ 1, 'asc' ]],
        "bDestroy": true,
        "lengthMenu": [[20, 50, 100, -1], [20, 50, 100, "Tümü"]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.11.5/i18n/tr.json"
        },
    });
    //Select Rows
    $("#tableRowNumber").text("Seçilen Satır Sayısı: " + 0);
    table.on( 'select', function ( e, dt, type, indexes ) {
        document.getElementById("allRemove").style.display='block';
        var count = table.rows( { selected: true } ).count();
        $("#tableRowNumber").text("Seçilen Satır Sayısı: " + count);
    });
    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if( table.rows('.selected').data().length === 0){
            document.getElementById("allRemove").style.display='none';
        }
        var count = table.rows( { selected: true } ).count();
        $("#tableRowNumber").text("Seçilen Satır Sayısı: " + count);
    });
    $('#checkAllProducts').click(function(){
        if($(this).is(':checked')){
            table.rows().select();
            document.getElementById("allRemove").style.display='block';
        } else {
            table.rows().deselect();
            document.getElementById("allRemove").style.display='none';
        }
    });
    //Remove Rows
    $('#allRemove').click( function () {
        Swal.fire({
            title: 'Domain adresleri silinsin mi?',
            text: "Seçili domain adresleri ve bağlı olduğu subdomain adresleri kalıcı olarak veritabanından silinecektir.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sil',
            cancelButtonText: 'Vazgeç'
        }).then((result) => {
        if (result.isConfirmed) {
            var dataArr = [];
            $.each($("#dataTable tr.selected"),function(){
                dataArr.push($(this).find('td').eq(1).text()); 
            });
            table.rows('.selected').remove().draw( false );
            for (let i = 0; i < dataArr.length; i++) {
                window.location = "/delete/"+dataArr;
            }
            Swal.fire(
            'Silindi!',
            'Domain adresleri başarıyla silindi.',
            'success'
            )
        }
        })
    } );
    //Add Rows
    $('#addRow').click( function () {
        Swal.fire({
            title: 'Domain adresi gir',
            input: 'text',
            inputAttributes: {
              autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Kaydet',
            cancelButtonText: 'Vazgeç',
            showLoaderOnConfirm: true,
            preConfirm: (name) => {
                document.getElementById('swal2-title').innerHTML = 'Subdomain adresleri taranıyor...Bu işlem biraz zaman alabilir.';
                document.getElementById('swal2-title').style.fontSize = "20px";
                document.querySelector('.swal2-cancel').style.display = "none";
              return fetch(`/add/${name}`)
                .then(response => {
                  if (!response.ok) {
                    throw new Error(response.statusText)
                  }
                  return response
                })
                .catch(error => {
                  Swal.showValidationMessage(
                    `Hata: ${error}`
                  )
                })
            },
            allowOutsideClick: () => {
                !Swal.isLoading()
            }
        }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Başarılı!',
                'Domain adresleri ve subdomain adresleri veritabanına eklendi.',
                'success'
                )
            .then(function(){ 
                location.reload();
                })
        }
        })
    } );
} );

//Subdomain List
function subFunction(dom, host) {
    $.ajax({
        type: "GET",
        url: "http://" + host + "/restapi/domains/?type=json&name=" + dom,
        data: { get_param: 'value' },
        dataType: 'json',
        success: function (data) { 
            if( data["results"][0]["subdomains"].length === 0){
                Swal.fire({
                    html: "Subdomain Bulunamadı.",
                    confirmButtonText: 'Kapat'
                })
            }
            else{
                var htmlData = document.createElement("ul");
                let nodes = data["results"][0]["subdomains"].map(lang => {
                    let li = document.createElement('li');
                    li.innerHTML= lang;
                    return li;
                });
                htmlData.append(...nodes);
                Swal.fire({
                    html: htmlData,
                    confirmButtonText: 'Kapat'
                })
            }
        },
        error: function(error){
            console.log("Error:");
            console.log(error);
        }
    });
};

//Name Servers List
function nsFunction(dom, host) {
    $.ajax({
        type: "GET",
        url: "http://" + host + "/restapi/domains/?type=json&name=" + dom,
        data: { get_param: 'value' },
        dataType: 'json',
        success: function (data) { 
            if( data["results"][0]["name_servers"] === "None"){
                Swal.fire({
                    html: "Name Servers Bulunamadı.",
                    confirmButtonText: 'Kapat'
                })
            }
            else{
                var htmlData = document.createElement("ul");
                let li = document.createElement('li');
                li.innerHTML= data["results"][0]["name_servers"];
                htmlData.append(li);
                Swal.fire({
                    html: htmlData,
                    confirmButtonText: 'Kapat'
                })
            }
        },
        error: function(error){
            console.log("Error:");
            console.log(error);
        }
    });
};

//Registrant Name
function rnFunction(dom, host) {
    $.ajax({
        type: "GET",
        url: "http://" + host + "/restapi/domains/?type=json&name=" + dom,
        data: { get_param: 'value' },
        dataType: 'json',
        success: function (data) { 
            if( data["results"][0]["registrant_name"] === ""){
                Swal.fire({
                    html: "Registrant Name Bulunamadı.",
                    confirmButtonText: 'Kapat'
                })
            }
            else{
                var htmlData = document.createElement("ul");
                let li = document.createElement('li');
                li.innerHTML= data["results"][0]["registrant_name"];
                htmlData.append(li);
                Swal.fire({
                    html: htmlData,
                    confirmButtonText: 'Kapat'
                })
            }
        },
        error: function(error){
            console.log("Error:");
            console.log(error);
        }
    });
};