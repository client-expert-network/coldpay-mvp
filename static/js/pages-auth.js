/**
 *  Pages Authentication
 */

'use strict';
const formAuthentication = document.querySelector('#formAuthentication');

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    // Form validation for Add new record
    if (formAuthentication) {
      const fv = FormValidation.formValidation(formAuthentication, {
        fields: {
          username: {
            validators: {
              notEmpty: {
                message: 'Please enter username'
              },
              stringLength: {
                min: 6,
                message: 'Username must be more than 6 characters'
              }
            }
          },
          email: {
            validators: {
              notEmpty: {
                message: '이메일을 입력해주세요'
              },
              emailAddress: {
                message: '올바른 이메일 주소를 입력해주세요'
              }
            }
          },
          'email-username': {
            validators: {
              notEmpty: {
                message: 'Please enter email / username'
              },
              stringLength: {
                min: 6,
                message: 'Username must be more than 6 characters'
              }
            }
          },
          password: {
            validators: {
              notEmpty: {
                message: '비밀번호를 입력해주세요'
              },
              stringLength: {
                min: 8,
                max: 32,
                message: '비밀번호는 8자 이상입니다'
              },
              regexp: {
                regexp: /^(?:(?=.*[A-Za-z])(?=.*\d)|(?=.*[A-Za-z])(?=.*[!@#$%^&*(),.?":{}|<>])|(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]))[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,32}$/,
                message: '비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 포함해야 합니다.'
              },
            }
          },
          'confirm-password': {
            validators: {
              notEmpty: {
                message: '비밀번호를 다시 입력해주세요'
              },
              identical: {
                compare: function () {
                  return formAuthentication.querySelector('[name="password"]').value;
                },
                message: '비밀번호가 일치하지 않습니다'
              },
              stringLength: {
                min: 8,
                message: '비밀번호는 8자 이상입니다'
              }
            }
          },
          terms: {
            validators: {
              notEmpty: {
                message: '약관에 동의해주세요'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-6'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }

    //  Two Steps Verification
    const numeralMask = document.querySelectorAll('.numeral-mask');

    // Verification masking
    if (numeralMask.length) {
      numeralMask.forEach(e => {
        new Cleave(e, {
          numeral: true
        });
      });
    }
  })();
});
