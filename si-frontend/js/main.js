var token="";
var googleToken="";

function onSignIn(googleUser) {
 console.log("On Sign In");
  var profile = googleUser.getBasicProfile();

  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail());


  var profileAuth = googleUser.getAuthResponse();

  googleToken = profileAuth.id_token;
  console.log("token= " + googleToken);

  $.ajax({
        url:"http://localhost:5000/register",
        type:'POST',
        headers:{'Authorization':'Token ' + googleToken},
        dataType:'json',
        error: function(data) {
            login();
        },
        success: function(data) {
            login();
        }
  })
  //getUser();
  //$('body').load('userData.html');
}
function getBearer() {
  console.log("bearerToken =" + token);
}
function login() {
     $.ajax({
        url:"http://localhost:5000/login",
        type:'GET',
        headers:{'Authorization':'Token ' + googleToken},
        dataType:'json',
        success: function(data) {
            token= data.access_token;
            getUser();
            $('body').load('userData.html');
        }
  })
}
function setup() {
 $.ajax({
        url: "http://localhost:5000/setup",
        type: 'GET',
        success: function(data) {
        $('body').load('#body');
                            }
        });
}
testData =null;

function getUser(){
$('body').load('userData.html');
$.ajax({
    url:"http://localhost:5000/me",
    headers:{'Authorization': 'Bearer ' + token},
    type:'GET',
    dataType: 'json',
    error: function(data) {
    errorMsg = data;
        console.log("errormsg= " + data);
         /**
         if(data.responseJSON.success == false) {
             $('body').load('userData.html');
          }
          **/
    },
    success: function(data) {
    userData = data;

    $('#userTableBody').append('<tr>'+
                    '<td href="#" onclick="getOrganizations()"><a id="userId" href="#"></a></td>'+

                    '<td id="userFirstname"></td>'+
                    '<td id="userLastname"></td>'+
                    '<td id="userEmail"></td>'+
                    '<td id="userGoogleId"></td>'+
                    '<td>'+
                        '<button onclick="editUserModal()"'+
                                'data-toggle="modal"'+
                                'data-target="#myModal"'+
                                'class="btn btn-default"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>'+
                        '</button>'+
                    '</td>'+
                    '<td>'+
                        '<button onclick="deleteUser()"'+
                                'class="btn btn-default"><span class="glyphicon glyphicon-remove"></span>'+
                        '</button>'+
                    '</td>'+
                '</tr>')
            $('#userFirstname').text(userData.firstname);
            $('#userLastname').text(userData.lastname);
            $('#userEmail').text(userData.email);
            $('#userId').text(userData.id);
            $('#userGoogleId').text(userData.google_id)
    }
})
}

function loadCreateOrganization() {
    $('body').load('createOrganization.html');
}
function getOrganizations() {
      loadCreateOrganization();
      $.ajax({
        url:"http://localhost:5000/me/organizations",
        headers:{'Authorization': 'Bearer ' + token},
        type:'GET',
        dataType:'json',
        success: function(data) {
           if(data.length != 0) {
           $('#tbodyOrganizations').empty();
              for(i=0; i< data.length; i++)  {
                    $('#tbodyOrganizations').append('<tr><td><a href="#" onclick="getOrganizationMember('+data[i].id+')">'+data[i].id+'</a></td><td id="organizationName'+data[i].id+'">'+data[i].name+'</td>'+
                                                        '<td class="editTd"><button data-toggle="modal" data-target="#orgModal" onclick="selectOrganization('+data[i].id+')" class="editBtn btn btn-default"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button></td>'+
                                                        '<td class="removeTd"><button onclick="removeOrganization('+data[i].id+')" class="removeBtn btn btn-default"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>'+
                                                    '</tr>');
                }
            }
        }
      });
}
function createOrganization() {
inputName =$('#inputNameOrganization').val();
    $.ajax({
        url:"http://localhost:5000/me/organizations",
        headers:{'Authorization': 'Bearer ' + token},
        data:{'name' : inputName},
        type:'POST',
        dataType:'json',
        success: function(data) {
        orgData = data;
        getOrganizations();

        }
    })
    }
function deleteUser() {
     $.ajax({
        url:"http://localhost:5000/me",
        headers:{'Authorization': 'Bearer ' + token},
        type:'DELETE',
        dataType:'json',
        success: function(data) {
            getUser();
        }
    })
}
function editUserModal(){
    $('#modalInputUserFirstname').attr('value',$('#userFirstname').text());
    $('#modalInputUserEmail').attr('value',$('#userEmail').text());
    $('#modalInputUserLastname').attr('value',$('#userLastname').text());
}

function submitUserChanges() {
    $.ajax({
    url:"http://localhost:5000/me",
    headers:{'Authorization':'Bearer ' + token},
    data:{'firstname': $('#modalInputUserFirstname').val(),
          'lastname':  $('#modalInputUserLastname').val(),
          'email': $('#modalInputUserEmail').val() },
    type:'PUT',
    dataType:'json',
    success: function(data){

        getUser();
    }

    })
//$('.alert-success').fadeIn().delay(1000).fadeOut();
}

function goToHome() {
    getUser();
}
function submitOrganizationChanges() {

    $.ajax({
        url:"http://localhost:5000/organizations/"+selectedOrgId,
        headers:{'Authorization': 'Bearer ' + token},
        data:{'name': $('#nameEditOrganization').val()},
        type:'PUT',
        dataType:'json',
        success: function(data) {
           getOrganizations();
        }
    })
    selectedOrgId=0;
}

selectedOrgId = 0;

function selectOrganization(id) {
    selectedOrgId=id;
    $('#nameEditOrganization').attr("value",$('#organizationName'+selectedOrgId).text());
}

function removeOrganization(id) {
     $.ajax({
        url:"http://localhost:5000/organizations/"+id,
        headers:{'Authorization': 'Bearer ' + token},
        type:'DELETE',
        dataType:'json',
        success: function(data) {
           getOrganizations();
        }
     })
}
organizationId =0;
function getOrganizationMember(id) {
organizationId = id;
 $('body').load('organization.html');
    $.ajax({
    url:"http://localhost:5000/organizations/"+organizationId+"/members",
    headers:{'Authorization':'Bearer ' + token},
    type: 'GET',
    dataType:'json',
    success: function(data){
       emptyTbodyOrgMember();
       for(i =0; i < data.length;i++) {
        appendMember(data[i]);

       }

       getInvitation(id);
           }
    })
}
function emptyTbodyOrgMember() {
    $('#tbodyOrgMember').empty();
}
function appendMember(member) {
    $('#tbodyOrgMember').append('<tr><td>'+ member.id+'</td><td>'+member.firstname+'</td><td>'+member.lastname+'</td><td>'+member.type+'</td></tr>');
}
function sendInvitation() {
    email = $('#emailForInvit').val();
     $.ajax({
    url:"http://localhost:5000/organizations/"+organizationId+"/invitations",
    headers:{'Authorization':'Bearer ' + token},
    data:{'email': email},
    type: 'POST',
    dataType:'json',
    success: function(data){
       alert("Invitation Sent");
       emptyTbodyOrgInvitation();
       getInvitation(organizationId);
           }
    })
}

function getInvitation(id){
console.log("getInvit!");
     $.ajax({
    url:"http://localhost:5000/organizations/"+id+"/invitations",
    headers:{'Authorization':'Bearer ' + token},
    type: 'GET',
    dataType:'json',
    success: function(data){
        console.log(data);
        for(i =0; i< data.length;i++) {
          appendInvitation(data[i]);
        }
    }
    })
}
function emptyTbodyOrgInvitation() {
    $('#tbodyOrgInvitation').empty();
}
function appendInvitation(invitation) {
     $('#tbodyOrgInvitation').append('<tr><td>'+ invitation.id+'</td><td>'+invitation.email+'</td><td>'+invitation.status+'</td><td></tr>');
}

$('#member a[href="#member"]').tab('show') ;
$('#invitation a[href="#invitation"]').tab('show');
$('#circle a[href="#circle"]').tab('show');
