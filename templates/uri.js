{% load staticfiles %}
$.uri = function(url){
    console.log('{% static '' %}' + url);
    return '{% static '' %}' + url;
}