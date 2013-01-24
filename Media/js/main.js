var DropDownFilterPannel = function(){

    var _data = [];

    var _option= {
        "pannel_height" : 300,
        "title" : "标题",
        "filter_input_placeholder" : "Filter",
        "filter_from_attribute" : "value",
        "click_handler" : function(el){},
        "init_value" : ""
    }
                
    var _template = '<div>'+
        '<div class="context-title"><span class="title"></span>'+
        '</div>'+
        '<div class="context-filter">'+
            '<input class="filter-input" placeholder="Fitler">'+
        '</div>'+
        '<div class="tabbable">'+
          '<div class="tab-content">'+
            '<ul class="tab-panel"></ul>'
          '</div>'+
        '</div>'+
      '</div>'


    var _buildBox = function(data){

        var box    = $(_template);
        var pannel = $(".tab-panel", box);
        $(data).each(function(index, item){
            var attributes = item["attributes"]
            var li = $('<li><a href="#"><span class="mini-icon mini-icon-confirm" style="visibility:hidden"></span><span class="text"></span></a></li>');
            var a  = $("a", li);
            for(k in attributes){
                li.attr("data-"+k, attributes[k])
            }

            if(item["name"] == _option["init_value"]){
                $(".mini-icon-confirm", li).css("visibility","visible");
            }

            $(".text", a).html(item["name"]);
            li.appendTo(pannel);

            a.click(function(event){
              event.preventDefault();
              var s = box.parent().parent().children(":first")
              s.html($(".text", a).html());
              box.parent().hide();

              $(".mini-icon", pannel).css("visibility","hidden");
              $(".mini-icon", this).css("visibility","visible");
            });

        });
        return box;
    }

    var _buildFilter = function(box){

        var filter_data = [];
        $(_data).each(function(index, item){
            filter_data.push(item["attributes"][_option["filter_from_attribute"]])
        });

        $('.filter-input', box).keyup(function(event){
          var keyword = $(this).val().toLowerCase();
          if ($.trim(keyword).length < 1) {
            $(".tab-content li", box).show();
          };

          $(".tab-content li", box).hide();

          $(filter_data).each(function(index,item){
            if(item.indexOf(keyword) > -1){
              console.log($('.tab-content li[data-'+_option["filter_from_attribute"]+'="'+item+'"]', box))
              $('.tab-content li[data-'+_option["filter_from_attribute"]+'="'+item+'"]', box).show();
            }
          });

      });

    }

    return {
        create : function(target, data, option){
            
            _data = data;
            $.extend(_option, option)

            var box = _buildBox(data);
            box.appendTo($(target));

            _buildFilter(box);

            $(".tab-panel", box).css("height", _option["pannel_height"]);
            $(".context-title span.title", box).html(_option["title"]);
            $(".filter-input", box).attr("placeholder", _option["placeholder"]);
        
            $(".tab-panel li", box).click(function(){
                _option["click_handler"]($(this));
            });
        }
    }

}
var FilterDropDown = function(){
    var _branches = [];
    var _tags = [];
    var _active = null;

    var _main = function(block){
      $('.filter-bt-handler').click(function(event){
          event.preventDefault();
          event.stopPropagation();
          $("#filterBandT").show();
          var position = $(this).offset();
          $("#filterBandT").css({
            left : position.left,
            top  : position.top + $(this).outerHeight() + 5
          });
          _active = $(this);
      });

      $('#filterBandT .filter-input').keyup(function(event){
          var keyword = $(this).val();
          $("#filterBandT .tab-content li").hide();
          $(branches).each(function(index,item){
            if(item.indexOf(keyword) > -1){
              $('#filterBandT .tab-content li[data-name="'+item+'"]').show();
            }
          });
          $(tags).each(function(index,item){
            if(item.indexOf(keyword) > -1){
              $('#filterBandT .tab-content li[data-name="'+item+'"]').show();
            }
          });
          if ($.trim(keyword).length < 1) {
            $("#filterBandT .tab-content li").show();
          };
      });
      $('#filterBandT .js-menu-close').click(function(event){
          event.preventDefault();
          $('#filterBandT').hide();
      });
      $(document).click(function(event){
          $('#filterBandT').hide();
      });
      $("#filterBandT").click(function(event){
          event.stopPropagation();
      });
      $(".nav-tabs a[data-toggle='tab-panel']").click(function(event){
          event.preventDefault();
          $(".nav-tabs a[data-toggle='tab-panel']").each(function(index,item){
            $(item).parent().removeClass('active');
          });
          $(".tab-content .tab-panel").hide();
          $("#"+$(this).attr('href').replace("#","")).show();
          $(this).parent().addClass('active');
      });

      $("#filterBandT .tab-panel li a").click(function(event){
            if (block) {
              block($(this), _active, event);
            } 
      });
    }

    return {

      "init" : function(branches, tags, block){

        _branches = branches;
        _tags   = tags;

        _main(block);
      },

      "hide" : function(){
        $("#filterBandT").hide();
      }
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var gpapi = function(option){

  var _option = {
    type : "POST",
    success : function(data){},
    dataType : "json"
  }

  _option = $.extend(_option, option)

  return {

    send : function(data){
      $.ajax({
        type: _option["type"],
        url: _option["url"],
        data: data,
        success: function(data){
          if (data["status"]=="fail") {
            if (data["messages"]) {
              var messages = data.messages;
              var html = ''
              $(messages).each(function(index, message){
                
                $(message.msg).each(function(index, item){
                  html+='<div class="alert alert-'+message.type+'">'+
                  '<button type="button" class="close" data-dismiss="alert">×</button>'+
                  '<strong>'+item[0]+': </strong>' + item[1] +
                  '</div>'
                })
              });
            };

            $(".error-messages").html(html);
            return;
          }

          _option.success(data);
        },
        dataType: "json"
      });
    }    
  }

}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

function arrays_equal(a,b) { return !(a<b || b<a); }

$(document).ready(function(){
  $( ".js-user-filter" ).autocomplete({
      source: function( request, response ) {
        $.ajax({
          type : "POST",
          url: "/accounts/filter",
          dataType: "json",
          data: {
            keywords : request.term
          },
          success: function( data ) {
            response( $.map( data.users, function( item ) {
              return {
                label: item.first_name,
                value: item.username
              }
            }));
          }
        });
      },
      minLength: 1,
      
      open: function() {
        //$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
      },
      close: function() {
        //$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
      }
    });

  $('[data-toggle="dropdown-filter"]').click(function(){
     event.preventDefault();
     var pannel = $(".dropdown-menu", $(this).parent());
     pannel.show();
     _this = this;
     $(document).click(function(e){
        var targets = $("*",pannel);
        $.extend(targets, [_this, pannel]);

        var is_target = false;
        $(targets).each(function(index, target){
          if($(e.target).is(target)) is_target = true;
        });
        if (is_target) return;
        pannel.hide();
    });
  });

});