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
    when lawyer clicked the upload button in edit photo box(profile)
    first ajax call will check the session timeout,
    if success, it will triggered the second ajax call.
    if NG, redirect to the home page

*/
function ajaxCall_profilePhotoCommit(url_profile){
    $('#editPhotoCommit').on('click', function(){
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
        
        var fileInput = document.getElementById('id_photos');
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('imgFile', file);
        formData.append('photo_edit_commit', 'action');
        
        $.ajax({
            type: "POST",
            url: url_profile,
            processData: false,   // tell jQuery not to process the data as string
            contentType: false,   // tell jQuery not to set contentType
            data: formData,
            success: function(data, textStatus, jqXHR){
                if(is_ajax_session_timeout(data)){
                    $('#session-body').html(data.message);
                    $('#session-title').html(data.title);
                    $('#sessionModal').modal('show');
                }else{
                    if(data.result == 'Failed'){
                        $('#m-title-msg').html(data.title);
                        $('#m-body-msg').html(data.message);
                        $('#msgModal-header').attr('class', 'modal-header msg modal-header-danger');
                        $('#msgModal').modal('show');
                        
                        
                    }else if(data.result == 'Success'){
                        $('#m-title-msg').html(data.title);
                        $('#m-body-msg').html(data.message);
                        $('#msgModal-header').attr('class', 'modal-header msg modal-header-success');
                        $('#msgModal').modal('show');
                        
                        $('#lawyerHome-profile-img').attr("src", data.img_url);
                        $('#lawyerHome-profile-img').css('width', '150px');
                        $('#lawyerHome-profile-img').css('height', '200px');
                    }else{
                        $('#m-title-msg').html(data.title);
                        $('#m-body-msg').html(data.message);
                        $('#msgModal-header').attr('class', 'modal-header msg modal-header-danger');
                        $('#msgModal').modal('show');
                        
                    }
                    
                }
            }
        });
    
    });


}

/*
    used in lawyer_home/_profile.html
    when lawyer clicked the edit photo box(profile)
    first ajax call will check the session timeout,
    if success, it will triggered the second ajax call.
    if NG, redirect to the home page

*/

function ajaxCall_profilePhotoEdit(url_profile){
    $('#profile-photo-edit').on('click', function () {
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
            type: "POST",
            url: url_profile,
            data: {photo_fetch:'action'},
            success: function(data, textStatus, jqXHR){
                if(is_ajax_session_timeout(data)){
                    $('#session-body').html(data.message);
                    $('#session-title').html(data.title);
                    $('#sessionModal').modal('show');
                    
                }else{
                
                    var photoForm = document.getElementById("editPhotoBox");
                    while (photoForm.hasChildNodes()) {
                        photoForm.removeChild(photoForm.lastChild);
                    }
                    $('#editPhotoModal').modal('show');
                    $('#editPhotoBox').append(data);
                
                }
            }
        });
        
        
        
    });
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
        
        $.ajax({
            type: 'POST',
            url: url_profile,
            data: {editCommit:'action',
                   form:JSON.stringify(json_object.serializeArray())
            },
            success: function(data, textStatus, jqXHR) {
                if(is_ajax_session_timeout(data)){
                    $('#session-body').html(data.message);
                    $('#session-title').html(data.title);
                    $('#sessionModal').modal('show');
                }else{
                    if(data.result == 'success'){
                        $('#m-body-msg').html(data.message);
                        $('#m-title-msg').html(data.result);
                        var tmpLawyerName = data.first_name + ' ' + data.last_name + '律師'
                        $('#lawyer-profile-name').html(tmpLawyerName);
                        
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
                                $('#msgModal-header').attr('class', 'modal-header msg modal-header-success');
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
                    $('#session-body').html(data.message);
                    $('#session-title').html(data.title);
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
                if(is_ajax_session_timeout(data)){
                    $('#session-body').html(data.message);
                    $('#session-title').html(data.title);
                    $('#sessionModal').modal('show');
                }else{
                    $('#m-body').append('<div id="fadeOut" class="alert alert-' + data.result+ '">' + data.message + '</div>');
                    $('#service-'+ data.type + ' .service-content').html(data.contents);
                    setTimeout(function(){
                        $('#fadeOut').fadeOut("slow", function(){
                            $('#fadeOut').remove();
                        });
                    }, 1000);
                }
                
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

/*

*/
function mail_consulting(url_consult){
    $('#mailModal').on('click', function(){
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
            url: url_consult,
            data: {mail_consult_fetch:'action'},
            success: function(data, textStatus, jqXHR) {
                var inquiryForm = document.getElementById("mailConsultBody");
                while (inquiryForm.hasChildNodes()) {
                    inquiryForm.removeChild(inquiryForm.lastChild);
                }
            
                $('#mailConsultTitle').html('送郵件給律師');
                $('#mailConsultBody').append(data);
                $('#mailConsultModal').modal('show');
                
            },
            error:function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });<!-- end of ajax-->
        
        
        
    });
}

function phone_consulting(){
    $('#phoneModal').on('click', function(){
        $('#phoneConsultTitle').html('打電話給律師');
        $('#phoneConsultBody').append('saaaa');
        $('#phoneConsultModal').modal('show');
    
    
    });

}
