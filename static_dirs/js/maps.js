$(function(){
    var map=new google.maps.Map($('#map')[0], {
        center:new google.maps.LatLng(-15.8419612,-70.0176313),
        zoom:16//,
        //scrollwheel:false
    });

    var map_residencia= new google.maps.Map($('#map-residencia')[0], {
        center: new google.maps.LatLng(-15.8419612,-70.0176313),
        zoom: 16
    });

    google.maps.event.addListener(map_residencia, "idle", function(){
        google.maps.event.trigger(map_residencia, 'resize');
    });

    var infowindow = new google.maps.InfoWindow({
        content: '',
        maxWidth: 350,
        width:350
    });

    google.maps.event.addListener(infowindow, 'domready', function(){
        var iwOuter = $('.gm-style-iw');
        var iwBackground = iwOuter.prev();
        iwBackground.children(':nth-child(2)').css({'display' : 'none'});
        iwBackground.children(':nth-child(4)').css({'display' : 'none'});
        //iwOuter.parent().parent().css({left: '115px'});
        //iwBackground.children(':nth-child(1)').attr('style', function(i,s){ return s + 'left: 76px !important;'});
        //iwBackground.children(':nth-child(3)').attr('style', function(i,s){ return s + 'left: 76px !important;'});
        iwBackground.children(':nth-child(3)').find('div').children().css({'box-shadow': 'rgba(72, 181, 233, 0.6) 0px 1px 6px', 'z-index' : '1'});
        var iwCloseBtn = iwOuter.next();
        iwCloseBtn.css({opacity: '1', right: '38px', top: '3px', border: '7px solid #48b5e9', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9', 'padding':'6.5px'});
        if($('.iw-content').height() < 140){
          $('.iw-bottom-gradient').css({display: 'none'});
        }
        iwCloseBtn.mouseout(function(){
          $(this).css({opacity: '1'});
        });
    });

    var size ={
        x: 30,
        y: 40
    };

    var icons={
        '1':{
            url: $.uri('img/icons/green.png'),
            size: new google.maps.Size(size.x, size.y),
            scaledSize: new google.maps.Size(size.x, size.y),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(size.x/2, size.y)
        },
        '2':{
            url: $.uri('img/icons/blue.png'),
            size: new google.maps.Size(size.x, size.y),
            scaledSize: new google.maps.Size(size.x, size.y),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(size.x/2, size.y)
        },
        '3':{
            url: $.uri('img/icons/red.png'),
            size: new google.maps.Size(size.x, size.y),
            scaledSize: new google.maps.Size(size.x, size.y),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(size.x/2, size.y)
        },
        '4':{
            url: $.uri('img/icons/yellow.png'),
            size: new google.maps.Size(size.x, size.y),
            scaledSize: new google.maps.Size(size.x, size.y),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(size.x/2, size.y)
        },
        'Masculino':{
            url: $.uri('img/icons/man.png'),
        },
        'Femenino':{
            url: $.uri('img/icons/woman.png'),
        },
        'Masculino y Femenino':{
            url: $.uri('img/icons/wym.png'),
        }
    };

    var nueva_residencia_marker = new google.maps.Marker({
        position: {
            lat: -15.8419612,
            lng: -70.0176313
        },
        title: 'Nueva Residencia',
        icon: icons['1'],
        draggable:true
    });

    nueva_residencia_marker.setMap(map_residencia);

    var update_nueva_residencia = function(){
        $('#latitud').val(nueva_residencia_marker.getPosition().lat());
        $('#longitud').val(nueva_residencia_marker.getPosition().lng());
    }

    google.maps.event.addListener(nueva_residencia_marker, 'dragend', function(e){
        update_nueva_residencia();
    });

    var updateMap = function(){
        $.ajax({
            url: $.uri('../residencias/form/search/'),
            data:$('#form-filtro').serialize(),
            type:'get',
            dataType: 'json',
            success:function(json){
                updateMarkers(json);
            }
        });
    }

    updateMap();

    var markers = [];

    var updateMarkers = function(json){
        var html = '';
        for(var i=0; i<markers.length; i++)
            markers[i].setMap(null);
        markers=[];
        $.each(json, function(){
            var $this = this;
            //console.log($this.fields);
            var marker = new google.maps.Marker({
                position: {
                    lat: $this.fields.latitude,
                    lng: $this.fields.longitude
                },
                title: $this.fields.description,
                icon: icons[$this.fields.tipo_residencia]
            });
            marker.addListener('click', function() {
                var content = '<div id="iw-container">' +
                    '<div class="iw-title">'+$this.fields.title+'</div>' +
                    '<div class="iw-content">' +
                      '<div class="iw-subTitle">Descripción</div>' +
                      '<p>'+$this.fields.description+'</p>' +
                      '<div class="iw-subTitle">Precios</div>'+
                      '<p>Desde: '+$this.fields.price_from+'<br>'+
                      'Hasta: '+$this.fields.price_until+'<br></p>'+
                      '<div class="iw-subTitle">Contacto</div>';
                content += '<p>';
                content += 'Dirección: '+$this.fields.address+'<br>'
                if($this.fields.phone2==null){
                    content += 'Telefono: '+$this.fields.phone1+'<br>'
                }else{
                    content += 'Telefono 1: '+$this.fields.phone1+'<br>'
                    content += 'Telefono 2: '+$this.fields.phone2+'<br>'
                }
                if($this.fields.email!=null)
                    content += 'E-mail: '+$this.fields.email+'<br>';
                content += '</p>';
                    '</div>' +
                    '<div class="iw-bottom-gradient"></div>' +
                  '</div>';
                infowindow.setContent(content);
                infowindow.open(map, marker);
            });
            marker.setMap(map);
            markers.push(marker);
            html += '<tr>';
            html += '<td> <img width="24" src="'+icons[$this.fields.tipo_residencia].url+'"></td>';
            html += '<td>'+$this.fields.title+'</td>';
            html += '<td> <img width="24" src="'+icons[$this.fields.gender].url+'"></td>';
            html += '</tr>';
        });
        $('#lista-residencias').html(html);
    }

    $('.sede').click(function(e){
        e.preventDefault();
        var $this = $(this);
        map.setCenter(new google.maps.LatLng($this.data('lat')*1, $this.data('lng')*1), 16);
    });

    $('#modal-nueva-residencia').click(function(e){
        e.preventDefault();
        $('#nueva-residencia').foundation('reveal', 'open');
        update_nueva_residencia();
        map_residencia.fitBounds(map_residencia.getBounds());
        google.maps.event.trigger(map_residencia, 'resize');
        map_residencia.setCenter(nueva_residencia_marker.getPosition());
        map_residencia.setZoom(16);
        $('#form-nueva-residencia').trigger("reset");
    });

    //google.maps.event.trigger(map, 'resize');

    $('#form-nueva-residencia').submit(function(e){
        e.preventDefault();
        var $this = $(this);
        $.ajax({
            url:$.uri('../residencias/form/save'),
            data:$this.serialize(),
            type:'get',
            dataType:'json',
            success:function(r){
                updateMap();
                $('#nueva-residencia').foundation('reveal', 'close');
            }
        });
    });

    $('#form-filtro').submit(function(e){
        e.preventDefault();
        updateMap();
    });

});
