$(document).ready(function(){
    var menu_visible = false;
    
    $('#projects_menu li').hover(function(){
        $(this).css('color', '#ccc');
    }, function(){
        $(this).css('color', 'white');

    });

    close_menu = function(){
        $('#projects_menu').css('display', 'none');
        menu_visible = false;
       
    }
    open_menu = function(){
        $('#projects_menu').css('display', 'block');
        menu_visible = true;
        
    }

    $('body').click(function(){
        close_menu();
    });

    $('#current_project_container').click(function(e){
        e.stopPropagation();
    });

    $('#projects_menu').click(function(e){
        e.stopPropagation();
    });

    $('#current_project_container').click(function(){
        if(!menu_visible){
            open_menu();
        } else{
            close_menu();
        }

    });
});


