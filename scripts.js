function redraw(e){
    var target = e.target;
    if (target.checked == false) {
        var elements = document.getElementsByClassName(target.id);
        for (var i=0; i<elements.length; i++){
            elements[i].style.visibility = "hidden";
        }
    }
    if (target.checked == true) {
        var elements = document.getElementsByClassName(target.id);
        for (var i=0; i<elements.length; i++){
            elements[i].style.visibility = "visible";
            elements[i].style.opacity = 0.7;
        }
    }
}


function toggle_check(e){
    value = document.getElementById(e.target.id).getAttribute('value');
        var inputs = document.getElementsByTagName('input');
        for(var i = 0; i < inputs.length; i++) {
            if(inputs[i].type == 'checkbox') {
                if (value == "clear")
                    inputs[i].checked = false;
                else
                    inputs[i].checked = true;
                var elements = document.getElementsByClassName(inputs[i].id);
                for (var j=0; j<elements.length; j++){
                if (value == "clear")
                    elements[j].style.visibility = "hidden";
                else
                    elements[j].style.visibility = "visible";
                    elements[j].style.opacity = 0.7;
                }
            }
        }
        if (value == "clear")
             document.getElementById(e.target.id).setAttribute('value', 'select all');
        else
             document.getElementById(e.target.id).setAttribute('value', 'clear');
    }


$(window).on('scroll', function () {
  var $w = $(window);
  $('.separator').css('top', $w.scrollTop());
});

$(document).ready(function(){

$('.tooltip').tooltipster({
                contentAsHTML: true,
                contentCloning: false,
                interactive: true,
                theme: 'tooltipster-borderless'
            });


$(window).load(function() {
        // Animate loading gif
        $(".se-pre-con").fadeOut("slow");
    });

$(".img").click(function(event) {
    var id = $(this).attr("id").split('_')[1] + "_" + $(this).attr("id").split('_')[2];
    var img_id = $(this).attr("id");
    var height = $("#container_"+id).height()
    image = new Image()
    image.src = $(this).attr("src")
    image.width = 500
    image.id = img_id
    console.log(img_id)
    if (height == 30){
        $("#container_"+id).animate({"height" : "500"}, 500);
        image.onload = function () {
                      $("#container_" + id).empty().append(image);
        }
    }
    else {
        current_img_id = $("#container_"+id).find("img").attr("id")
        if (current_img_id == img_id){
          $("#container_"+id).animate({"height" : "30"}, 500);
          $("#container_"+id).empty();
        }
        else {
          $("#container_" + id).empty().append(image);
        }
    }
});


$('#lanes').click( function() {
  var scroll_pos = $(window).scrollTop();
  console.log(scroll_pos)
  draw_orfs();
  $(window).scrollTop(scroll_pos);
  console.log($(window).scrollTop())
});

//DRAW ORFs
function draw_orfs(){
    show = $('#show').attr("value");
    $('.contig').each(
        function(){
            if (show == "strips"){
                $('#show').attr("value", "frames");
                $('#lanes').attr("src", "./track-strip.png");
                id = $(this).attr("id").split('_')[0] + "_" + $(this).attr("id").split('_')[1];
                bar = $('#' + id + "_bar");
                $('#' + id).attr("height", 90);
                $(bar).attr("height", 9);
                $(bar).attr("fill-opacity", 0.4);
                $(bar).attr("y", 38);
                $('.' + id + "_lane").attr("visibility", "visible");
                $('#' + id).find('g').each(
                    function(){
                        if ($(this).find('rect').length > 1){
                            r = $(this).find('rect')[0];
                            fill = $($(this).find('rect')[1]).attr("fill");
                            $($(this).find('rect')[1]).attr("fill-opacity", "0");
                            frame = $($(this).find('rect')[1]).attr("class");
                            x = $(r).attr("x");
                            if (fill == "green"){
                                if (frame == 1)
                                    $(r).attr("y", 10);
                                else if (frame == 2)
                                    $(r).attr("y", 20);
                                else
                                    $(r).attr("y", 30);
                               }
                            else {
                                if (frame == 1)
                                    $(r).attr("y", 50);
                                else if (frame == 2)
                                    $(r).attr("y", 60);
                                else
                                    $(r).attr("y", 70);
                            }
                            $(r).attr("height", 5);
                            color = $(this).attr("class").split(" ")[0];
                            $(r).attr("fill", color);

                        }
                        else{
                                r = $(this).find('rect')[0];
                                $(r).attr("height", 5);
                                $(r).attr("y", 40);
                            }
                    });
             }
            else {
                $('#show').attr("value", "strips");
                $('#lanes').attr("src", "./track-frames.png");
                id = $(this).attr("id").split('_')[0] + "_" + $(this).attr("id").split('_')[1];
                bar = $('#' + id + "_bar");
                $('.' + id + "_lane").attr("visibility", "hidden")
                $('#' + id).attr("height", 90);
                $(bar).attr("y", 50);
                $(bar).attr("height", 30);
                $(bar).attr("fill-opacity", 0.3);
                $('#' + id).find('g').each(
                    function(){
                        r = $(this).find('rect')[0];
                            $(r).attr("y", 50);
                            $(r).attr("height", 30);
                            color = $(this).attr("class").split(" ")[0];
                            $(r).attr("fill", color);
                            $($(this).find('rect')[1]).attr("fill-opacity", 0.7);

                 });
            }
        });
  }

$('.orfs').click(draw_orfs)
});
