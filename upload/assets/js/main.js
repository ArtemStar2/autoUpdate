$(document).ready(function() {
    function generateRandomFileName() {
        const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let randomFileName = '';
        for (let i = 0; i < 10; i++) {
          const randomIndex = Math.floor(Math.random() * chars.length);
          randomFileName += chars.charAt(randomIndex);
        }
        return randomFileName;
    }

    $('#form_custom, .form_custom').submit(function(e) {
        e.preventDefault();
        const form = $(this);

        const btn = form.find('button[type="submit"]');

        btn.attr("data-kt-indicator", "on");
        btn.attr("disabled", "disabled");

        form.find('.fv-plugins-message-container').remove();

        var formData = new FormData(this);

        if(formData.get('auto_greeting') && formData.get('auto_greeting') == "null"){
            
            formData.set('auto_greeting', "");
        }
        
        if(formData.get('mass_message') && formData.get('mass_message') == "null"){
            formData.set('mass_message', "");
        }        

        if(formData.get('dictionary')?.name == ""){
            formData.delete('dictionary');
        }

        if(!formData.get('auto_start_chat')){
            formData.set('auto_start_chat', "false");
        }

        if(!formData.get('endless_messages')){
            formData.set('endless_messages', "false");
        }

        if(form.hasClass("auth") && form.hasClass("register")){
            var recaptchaResponse = grecaptcha.getResponse();
        
            if (recaptchaResponse.length == 0) {
                alert('Ошибка заполнения капчи.');
                return;
            }
            $.ajax({
                url: 'https://www.google.com/recaptcha/api/siteverify',
                type: 'POST',
                crossDomain: true,
                dataType: 'json',
                headers: {
                    "Access-Control-Allow-Origin": "*"
                },
                data: {
                    secret: '6Lc7PQUpAAAAAG_hNixYGxgA7xMX4ypbLeipYLiX',
                    response: recaptchaResponse
                },
                success: function(response) {
                    console.log(response);
                    if (response.success) {
                        console.log("Daaa");
                    } else {
                        console.log('Ошибка заполнения капчи.');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(textStatus);
                    console.log(errorThrown)
                }
            });
        }

        $.ajax({
            type: form.attr("method") ? form.attr("method") :'POST',
            url: form.attr("action"),
            data: formData,
            contentType: false, // Не устанавливать Content-Type
            processData: false, // Не обрабатывать данные,
            enctype: "multipart/form-data",
            headers: {
                'Authorization': 'Bearer ' + KTCookie.get("access"),
                'X-CSRFToken' : form.find('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                if(form.hasClass("auth")){
                    KTCookie.set("access", data?.access);
                    KTCookie.set("refresh", data?.refresh);
                }

                Swal.fire({
                    text: data?.detail,
                    icon: "success",
                    buttonsStyling: !1,
                    confirmButtonText: "Перейти далее",
                    customClass: {
                        confirmButton: "btn btn-primary"
                    }
                }).then((function(e) {
                    if(form.hasClass("auth")){
                        window.location.href = '/';
                    }else{
                        location.reload();
                    }
                }))
            },
            error: function(jqXHR, textStatus, errorThrown) {
                const data = jqXHR.responseJSON;                
                if(errorThrown == "Forbidden" && !form.hasClass("auth")){
                    $.ajax({
                        url: '/v1/api/auth/refresh/',
                        method: 'POST',
                        data:{
                            refresh: KTCookie.get("refresh")
                        },
                        success: function(data) { 
                            KTCookie.set("access", data?.access);
                            $.ajax({
                                type: form.attr("method") ? form.attr("method") :'POST',
                                url: form.attr("action"),
                                data: formData,
                                contentType: false, // Не устанавливать Content-Type
                                processData: false, // Не обрабатывать данные,
                                enctype: "multipart/form-data",
                                headers: {
                                    'Authorization': 'Bearer ' + KTCookie.get("access"),
                                    'X-CSRFToken' : form.find('input[name="csrfmiddlewaretoken"]').val()
                                },
                                success: function(data) {
                                    if(form.hasClass("auth")){
                                        KTCookie.set("access", data?.access);
                                        KTCookie.set("refresh", data?.refresh);
                                    }
                    
                                    Swal.fire({
                                        text: data?.detail,
                                        icon: "success",
                                        buttonsStyling: !1,
                                        confirmButtonText: "Перейти далее",
                                        customClass: {
                                            confirmButton: "btn btn-primary"
                                        }
                                    }).then((function(e) {
                                        if(form.hasClass("auth")){
                                            window.location.href = '/';
                                        }else{
                                            location.reload();
                                        }
                                    }))
                                },
                                error: function(jqXHR, textStatus, errorThrown) {
                                    const data = jqXHR.responseJSON;                
                                    if(data?.detail){
                                        Swal.fire({
                                            text: data.detail,
                                            icon: "error",
                                            buttonsStyling: !1,
                                            confirmButtonText: "Повторить попытку",
                                            customClass: {
                                                confirmButton: "btn btn-primary"
                                            }
                                        })
                                    }else{
                                        for (item in data) {
                                            console.log(item, data[item]);
                                            let str = `<div class="fv-plugins-message-container fv-plugins-message-container--enabled invalid-feedback"><div data-field="${item}" data-validator="notEmpty">${data[item]}</div></div>`;
                    
                                            form.find('input[name="'+item+'"]').parent().append(str);
                                        }
                    
                                    }
                                },
                                complete: function(jqXHR, textStatus) {
                                    btn.attr("data-kt-indicator", "off");
                                    btn.removeAttr("disabled");
                                }
                            });
                        },
                        error: function(xhr, status, error) {
                            console.log(error);
                        }
                    });
                }else if(data?.detail){
                    Swal.fire({
                        text: data.detail,
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Повторить попытку",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }else{
                    for (item in data) {
                        console.log(item, data[item]);
                        let str = `<div class="fv-plugins-message-container fv-plugins-message-container--enabled invalid-feedback"><div data-field="${item}" data-validator="notEmpty">${data[item]}</div></div>`;

                        form.find('input[name="'+item+'"]').parent().append(str);
                    }

                }
            },
            complete: function(jqXHR, textStatus) {
                btn.attr("data-kt-indicator", "off");
                btn.removeAttr("disabled");
            }
        });
    });

    function sendAjaxRequest() {
        $.ajax({
            url: '/v1/api/bots/',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + KTCookie.get("access"),
            },
            success: function(data) { 
                str = "";
                data.forEach(element => {
                    
                    str += `
                        <div class="d-flex align-items-center flex-column mt-3 w-100">
                            <div class="d-flex justify-content-between w-100 mt-auto mb-2">
                                <span class="fw-bolder fs-6 text-dark">${element.name}:</span>
                                <span class="fw-bold fs-6 text-gray-400"><span class="fw-bolder fs-6 text-dark">${element.count} / </span> <span class="fw-bold fs-6 text-gray-400">${element.max_count}</span></span>
                            </div>
                            <div class="h-8px mx-3 w-100 bg-light-success rounded">
                                <div class="bg-success rounded h-8px" role="progressbar" style="width: ${Math.round((element.count / element.max_count) * 100)}%;" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </div>
                    `;
                });

                $('#dashboards-list').html("")
                $('#dashboards-list').html(str);
            },
            error: function(xhr, status, error) {
                // console.log(status);
                if(error == "Forbidden"){
                    $.ajax({
                        url: '/v1/api/auth/refresh/',
                        method: 'POST',
                        data:{
                            refresh: KTCookie.get("refresh")
                        },
                        success: function(data) { 
                            KTCookie.set("access", data?.access);
                            sendAjaxRequest();
                        },
                        error: function(xhr, status, error) {
                            console.log(error);
                        }
                    });
                }
                // console.log(error);
            }
        });
    }
    
    $('#cardlink_payment').submit(function(e) {
        e.preventDefault();
        const form = $(this);
        const amount = parseInt(form.find('input[name="price"]').val());

        if(!amount){
            Swal.fire({
                text: "Введите сумму",
                icon: "error",
                buttonsStyling: !1,
                confirmButtonText: "Повторить попытку",
                customClass: {
                    confirmButton: "btn btn-primary"
                }
            })
        }

        $.ajax({
            url: 'https://cardlink.link/api/v1/bill/create',
            type: 'POST',
            dataType: 'json',
            data: {
                amount: amount,
                shop_id: 'LXZv3R7Q8B',
                currency_in: "RUB"
            },
            success: function(response) {
                console.log(response)
                payment_user(amount, "credit", "Оплата CardLink")
            },
            error: function(jqXHR, textStatus, errorThrown) {
                payment_user(amount, "credit", "Оплата CardLink")
                // Swal.fire({
                //     text: "Ошибка:" + jqXHR.responseJSON.message,
                //     icon: "error",
                //     buttonsStyling: !1,
                //     confirmButtonText: "Повторить попытку",
                //     customClass: {
                //         confirmButton: "btn btn-primary"
                //     }
                // })
            }
        });
    });

    function payment_user(amount, transaction_type, description){
        $.ajax({
            url: '/v1/api/balance/',
            type: 'PUT',
            dataType: 'json',
            headers: {
                'Authorization': 'Bearer ' + KTCookie.get("access"),
                'X-CSRFToken' : KTCookie.get("csrftoken")
            },
            data: {
                amount: parseInt(amount),
                transaction_type: transaction_type,
                description: description
            },
            success: function(response) {
                Swal.fire({
                    text: "Транзакция завершена",
                    icon: "success",
                    buttonsStyling: !1,
                    confirmButtonText: "Перейти к покупкам",
                    customClass: {
                        confirmButton: "btn btn-primary",
                    }
                }).then((function(e) {
                    location.reload();
                }));
            },
            error: function(jqXHR, textStatus, errorThrown) {
                Swal.fire({
                    text: "Ошибка:" + jqXHR.responseJSON.message,
                    icon: "error",
                    buttonsStyling: !1,
                    confirmButtonText: "Повторить попытку",
                    customClass: {
                        confirmButton: "btn btn-primary"
                    }
                })
            }
        });
    }

    $('body').on('click', '.channel-delete-js' ,function (e) { 
        const id = $(this).attr('data-id');
        $.ajax({
            type: 'DELETE',
            url: '/v1/api/auth/channels/' + id + '/',
            headers: {
                'Authorization': 'Bearer ' + KTCookie.get("access"),
                'X-CSRFToken' : KTCookie.get("csrftoken")
            },
            success: function(data) {
                Swal.fire({
                    text: data?.detail,
                    icon: "success",
                    buttonsStyling: !1,
                    confirmButtonText: "Успешно удалено",
                    customClass: {
                        confirmButton: "btn btn-primary"
                    }
                });
                $.ajax({
                    type: 'GET',
                    url: '/v1/api/auth/channels/',
                    headers: {
                        'Authorization': 'Bearer ' + KTCookie.get("access"),
                        'X-CSRFToken' : KTCookie.get("csrftoken")
                    },
                    success: function(data) {
                        str = "";
                        data.forEach(element => {
                            str += `
                            <!--begin::Col-->
                            <div class="col-sm-6 col-xl-4">
                                <!--begin::Card-->
                                <div class="card h-100">
                                    <!--begin::Card header-->
                                    <div class="card-header flex-nowrap border-0 pt-9">
                                        <!--begin::Card title-->
                                        <div class="card-title m-0">
                                            <!--begin::Title-->
                                            <a href="${element.url}" target="_blank" class="fs-4 fw-semibold text-hover-primary text-gray-600 m-0">${element.channel_type}</a>
                                            <!--end::Title-->
                                        </div>
                                        <!--end::Card title-->
                                        <a href="#" class="menu-link flex-stack px-3 channel-delete-js" data-id="${element.id}">Удалить
                                            <span class="ms-2" data-bs-toggle="tooltip" title="Удалить канал">
                                                <i class="ki-duotone ki-information fs-6">
                                                    <span class="path1"></span>
                                                    <span class="path2"></span>
                                                    <span class="path3"></span>
                                                </i>
                                            </span>
                                        </a>
                                    </div>
                                    <!--end::Card header-->
                                    <!--begin::Card body-->
                                    <div class="card-body d-flex flex-column px-9 pt-6 pb-8">
                                        <!--begin::Heading-->
                                        <div class="fs-2tx fw-bold mb-3">${element.name_channel}</div>
                                        <div class="fs-4 fw-semibold text-gray-600 m-0">Подписчиков: ${element.subscribers}</div>
										<div class="fs-4 fw-semibold text-gray-600 m-0">Просмотров: ${element.views}</div>
                                        <!--end::Heading-->
                                    </div>
                                    <!--end::Card body-->
                                </div>
                                <!--end::Card-->									
                            </div>
                            <!--end::Col-->
                            `;
                        });

                        $('#list-channels').html("")
                        $('#list-channels').html(str);
                    }
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {          
                if(errorThrown == "Forbidden"){
                    $.ajax({
                        url: '/v1/api/auth/refresh/',
                        method: 'POST',
                        data:{
                            refresh: KTCookie.get("refresh")
                        },
                        success: function(data) { 
                            KTCookie.set("access", data?.access);
                            $.ajax({
                                type: 'DELETE',
                                url: '/v1/api/auth/channels/' + id + '/',
                                headers: {
                                    'Authorization': 'Bearer ' + KTCookie.get("access"),
                                    'X-CSRFToken' : KTCookie.get("csrftoken")
                                },
                                success: function(data) {
                                    Swal.fire({
                                        text: data?.detail,
                                        icon: "success",
                                        buttonsStyling: !1,
                                        confirmButtonText: "Успешно удалено",
                                        customClass: {
                                            confirmButton: "btn btn-primary"
                                        }
                                    });
                                    $.ajax({
                                        type: 'GET',
                                        url: '/v1/api/auth/channels/',
                                        headers: {
                                            'Authorization': 'Bearer ' + KTCookie.get("access"),
                                            'X-CSRFToken' : KTCookie.get("csrftoken")
                                        },
                                        success: function(data) {
                                            str = "";
                                            data.forEach(element => {
                                                str += `
                                                <!--begin::Col-->
                                                <div class="col-sm-6 col-xl-4">
                                                    <!--begin::Card-->
                                                    <div class="card h-100">
                                                        <!--begin::Card header-->
                                                        <div class="card-header flex-nowrap border-0 pt-9">
                                                            <!--begin::Card title-->
                                                            <div class="card-title m-0">
                                                                <!--begin::Title-->
                                                                <a href="${element.url}" target="_blank" class="fs-4 fw-semibold text-hover-primary text-gray-600 m-0">${element.channel_type}</a>
                                                                <!--end::Title-->
                                                            </div>
                                                            <!--end::Card title-->
                                                            <a href="#" class="menu-link flex-stack px-3 channel-delete-js" data-id="${element.id}">Удалить
                                                                <span class="ms-2" data-bs-toggle="tooltip" title="Удалить канал">
                                                                    <i class="ki-duotone ki-information fs-6">
                                                                        <span class="path1"></span>
                                                                        <span class="path2"></span>
                                                                        <span class="path3"></span>
                                                                    </i>
                                                                </span>
                                                            </a>
                                                        </div>
                                                        <!--end::Card header-->
                                                        <!--begin::Card body-->
                                                        <div class="card-body d-flex flex-column px-9 pt-6 pb-8">
                                                            <!--begin::Heading-->
                                                            <div class="fs-2tx fw-bold mb-3">${element.name_channel}</div>
                                                            <div class="fs-4 fw-semibold text-gray-600 m-0">Подписчиков: ${element.subscribers}</div>
                                                            <div class="fs-4 fw-semibold text-gray-600 m-0">Просмотров: ${element.views}</div>
                                                            <!--end::Heading-->
                                                        </div>
                                                        <!--end::Card body-->
                                                    </div>
                                                    <!--end::Card-->									
                                                </div>
                                                <!--end::Col-->
                                                `;
                                            });
                    
                                            $('#list-channels').html("")
                                            $('#list-channels').html(str);
                                        }
                                    });
                                },
                                error: function(jqXHR, textStatus, errorThrown) {          
                                    Swal.fire({
                                        text: "Ошибка",
                                        icon: "error",
                                        buttonsStyling: !1,
                                        confirmButtonText: "Повторить попытку",
                                        customClass: {
                                            confirmButton: "btn btn-primary"
                                        }
                                    })
                                }
                            });
                        },
                        error: function(xhr, status, error) {
                            console.log(error);
                        }
                    });
                }else{
                    Swal.fire({
                        text: "Ошибка",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Повторить попытку",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }  
            }
        });
    });

    $('body').on('input', '.range-js', function() {
        const value = $(this).find('input[type="range"]').val();
        $(this).find('.value-range').text(value); 
        const parent = $(this).parents('form.card-body');
        let cost_bost = parseInt(parent.find('input[name="count_minutes_cost"]').val()) * parseInt(parent.find('input[name="count_bots"]').val())
        let cost_minutes = parseInt(parent.find('input[name="count_minutes_cost"]').val()) * parseInt(parent.find('input[name="count_minutes"]').val())

        parent.find('.cost-all-card').text((cost_bost + cost_minutes) + ",0");
    });

    if($('#dashboards-list').html()){
        sendAjaxRequest();
        setInterval(sendAjaxRequest, 15000);
    }

    $('#logout-js').click(function(e) {
        e.preventDefault();
        KTCookie.remove("access");
        KTCookie.remove("refresh");
        window.location.href = '/';
    })
});