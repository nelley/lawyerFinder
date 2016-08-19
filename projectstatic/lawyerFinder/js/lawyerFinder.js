/*
    ajax session timeout checker
*/
function is_ajax_session_timeout(d){
    if(d.result == 'timeout'){
        return true;
    }else{
        return false;
    }

}

/*
    used in lawyer_home/_profile.html
    when lawyer clicked the save button(profile).
    First ajax call checks the session timeout.
    if OK, save the modification.
    if NG, show the session timeout dialog

*/
function ajaxCall_profileCommit(url_profile){
    $('#editProfileCommit').on('click', function () {
        $.ajaxSetup({ 
            beforeSend: function(xhr, settings) {
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
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });
        
        var json_object = $("#editProfileBox");
        //alert(JSON.stringify(json_object.serializeArray()));
        
        
        $.ajax({
            type: 'POST',
            url: url_profile,
            data: {editCommit:'action',
                   form:JSON.stringify(json_object.serializeArray())
            },
            success: function(data, textStatus, jqXHR) {
                if(is_ajax_session_timeout(data)){
                    $('#sessionModal').modal('show');
                }else{
                    if(data.result == 'success'){
                        $('#m-body-msg').html(data.message);
                        $('#m-title-msg').html(data.result);
                        
                        $.ajax({
                            type: "POST",
                            url: url_profile,
                            data: {profile_fetch:'action'},
                            success: function(data, textStatus, jqXHR){
                                var profileForm = document.getElementById("editProfileBox");
                                while (profileForm.hasChildNodes()) {
                                    profileForm.removeChild(profileForm.lastChild);
                                }
                                $('#editProfileBox').append(data);
                                
                                //show the msg modal
                                $('#msgModal').modal('show');
                                
                            }
                        });
                    }else{
                        var profileForm = document.getElementById("editProfileBox");
                        while (profileForm.hasChildNodes()) {
                            profileForm.removeChild(profileForm.lastChild);
                        }
                        $('#editProfileBox').append(data);
                    }
                    
                    
                    
                }
            },
            error:function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });<!-- end of ajax-->
    });

}



/*
    used in lawyer_home/_profile.html
    when lawyer clicked the edit box(profile)
    first ajax call will check the session timeout,
    if success, it will triggered the second ajax call.
    if NG, redirect to the home page

*/

function ajaxCall_profile(url_profile) {
    
    $('#profile-edit').on('click', function () {
        
        $.ajaxSetup({ 
            beforeSend: function(xhr, settings) {
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
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });
        $.ajax({
            type: 'POST',
            url: url_profile,
            data: {profile_fetch:'action'},
            success: function(data, textStatus, jqXHR) {
                
                if(is_ajax_session_timeout(data)){
                    $('#sessionModal').modal('show');
                }else{
                    $.ajax({
                        type: "POST",
                        url: url_profile,
                        data: {profile_fetch:'action'},
                        success: function(data, textStatus, jqXHR){
                            $('#editProfileModal').modal('show');
                            
                            var profileForm = document.getElementById("editProfileBox");
                            while (profileForm.hasChildNodes()) {
                                profileForm.removeChild(profileForm.lastChild);
                            }
                            $('#editProfileBox').append(data);
                        }
                    });
                }
                
            },
            error:function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });<!-- end of ajax-->
        
    });<!-- end of profile-edit-->
    
}
/*
    used in lawyer_home/_service.html
    when lawyer want to change their service content

*/
function ajaxCall_service_edit_commit(url_service) {
    
    $("#editCommit").on('click', function(){
        $.ajaxSetup({ 
            beforeSend: function(xhr, settings) {
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
                function updateCKEditor(){
                    for (instance in CKEDITOR.instances) {
                        CKEDITOR.instances[instance].updateElement();
                    }
                }
                
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                updateCKEditor();
            }
        });
        
        
        $.ajax({
            type: 'POST',
            url: url_service,
            data: {type:$('input[name=editType]').val(),
                   basic:CKEDITOR.instances.id_basic.getData(),
                   service_edit:'action'
                  },
            success: function(data, textStatus, jqXHR) {
                $('#m-body').append('<div id="fadeOut" class="alert alert-' + data.result+ '">' + data.message + '</div>');
                $('#service-'+ data.type + ' .service-content').html(data.contents);
                setTimeout(function(){
                    $('#fadeOut').fadeOut("slow", function(){
                        $('#fadeOut').remove();
                    });
                }, 1000);
                
                
                
                
            },
            error:function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });

}


/*
    used in lawyer_home/_service.html
    when lawyer edit their service,
    this function will get the clicked service title

*/
function get_service_title() {
    $("button[id*='c-']").on('click', function () {
            // change to s-1
            var clickedE= $(this).attr('id')
            var titleId = clickedE.replace('c' , 's');
            var title = document.getElementById(titleId).textContent;
            $('.modal-title.service').text(title);
            
            $('input[name=editType]').attr('value', clickedE.split('-')[1]);
            
            var textDisplay = $(this).parent().children().html();
            
            // init ckeditor's notent(id_basic is the id of textarea)
            CKEDITOR.instances.id_basic.setData( textDisplay, function(){
                this.checkDirty();  // true
            });
            
    });
}
