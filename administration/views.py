from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from lessons.models import Module, Lesson, Step
from home.models import AffiliateLinkControl
from topic.models import StepControl

from account import models as account_model
from account import forms as account_form

from home import models as home_model

from . import forms

from . import tasks

from . import email


class AdminPermission(PermissionRequiredMixin, View):
    permission_required = 'is_superuser'


class Index(AdminPermission, View):
    template_name = 'administration/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#all user
class AllUser(AdminPermission, View):
    template_name = 'administration/all-user.html'

    def get(self, request):

        all_users = account_model.UserProfile.objects.all()
        all_users_count = account_model.UserProfile.objects.all().count()

        variables = {
            'all_users': all_users,
            'all_users_count': all_users_count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#user detail
class UserDetail(AdminPermission, View):
    template_name = 'administration/user-detail.html'

    def get(self, request, user_id):

        user = get_object_or_404(account_model.UserProfile, pk=user_id)

        payments = account_model.Payment.objects.filter(user__id=user_id).order_by('-creation_time')


        variables = {
            'user': user,
            'payments': payments,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):
        pass



#edit user
class EditUser(AdminPermission, View):
    template_name = 'administration/user-edit.html'

    def get(self, request, user_id):

        user = get_object_or_404(account_model.UserProfile, pk=user_id)

        user_edit_form = account_form.UserEditForm(instance=account_model.UserProfile.objects.get(id=user_id))

        variables = {
            'user': user,
            'user_edit_form': user_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):
        user = get_object_or_404(account_model.UserProfile, pk=user_id)

        user_edit_form = account_form.UserEditForm(request.POST or None, request.FILES, instance=account_model.UserProfile.objects.get(id=user_id))

        if user_edit_form.is_valid():
            user_edit_form.save()

            return redirect('administration:user-detail', user_id=user.id)

        variables = {
            'user': user,
            'user_edit_form': user_edit_form,
        }

        return render(request, self.template_name, variables)



#change user password
class ChangeUserPassword(View):
    template_name = 'administration/change-user-password.html'

    def get(self, request, user_id):

        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        change_user_password = forms.ChangeUserPasswordForm()

        variables = {
            'users': users,
            'change_user_password': change_user_password,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):
        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        change_user_password = forms.ChangeUserPasswordForm(request.POST or None)

        if change_user_password.is_valid():
            change_user_password.deploy(user_id)

        variables = {
            'users': users,
            'change_user_password': change_user_password,
        }

        return render(request, self.template_name, variables)




#active or deactive user
class ActiveDeactiveUser(AdminPermission, View):
    template_name = 'administration/activate-deactivate-user.html'

    def get(self, request, profile_status, user_id):

        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        variables = {
            'users': users,
            'profile_status': profile_status,
        }

        return render(request, self.template_name, variables)

    def post(self, request, profile_status, user_id):
        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        if request.POST.get('yes') == 'yes':
            for user in users:
                if profile_status == 'activate':
                    user.is_active = True
                    user.save()
                elif profile_status == 'deactivate':
                    user.is_active = False
                    user.save()
            return redirect('administration:user-detail', user_id=user_id)

        elif request.POST.get('no') == 'no':
            return redirect('administration:user-detail', user_id=user_id)


        variables = {
            'users': users,
            'profile_status': profile_status,
        }

        return render(request, self.template_name, variables)




#delete user
class DeleteUser(AdminPermission, View):
    template_name = 'administration/delete-user.html'

    def get(self, request, user_id):

        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        variables = {
            'users': users,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):
        get_object_or_404(account_model.UserProfile, pk=user_id)
        users = account_model.UserProfile.objects.filter(id=user_id)

        if request.POST.get('yes') == 'yes':
            users.delete()
            return redirect('administration:all-user')

        elif request.POST.get('no') == 'no':
            return redirect('administration:all-user')

        variables = {
            'users': users,
        }

        return render(request, self.template_name, variables)



#change membership
class ChangeMembership(AdminPermission, View):
    template_name = 'administration/change-membership.html'

    def get(self, request, user_id):

        user = get_object_or_404(account_model.UserProfile, pk=user_id)

        change_membership_form = forms.ChangeMembershipForm(instance=account_model.UserProfile.objects.get(id=user_id))

        variables = {
            'user': user,
            'change_membership_form': change_membership_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):
        user = get_object_or_404(account_model.UserProfile, pk=user_id)

        change_membership_form = forms.ChangeMembershipForm(request.POST or None, instance=account_model.UserProfile.objects.get(id=user_id))

        if change_membership_form.is_valid():
            change_membership_form.save()

            user_obj = account_model.UserProfile.objects.get(id=user_id)
            user_obj.package_buy_time = datetime.datetime.now()
            user_obj.save()

            return redirect('administration:user-detail', user_id=user.id)

        variables = {
            'user': user,
            'change_membership_form': change_membership_form,
        }

        return render(request, self.template_name, variables)



#payment
#pending payment
class PaymentPending(AdminPermission, View):
    template_name = 'administration/pending-payment.html'

    def get(self, request):

        pending_payments = account_model.Payment.objects.filter(is_verify='pending')
        pending_payment_count = account_model.Payment.objects.filter(is_verify='pending').count()

        variables = {
            'pending_payments': pending_payments,
            'pending_payment_count': pending_payment_count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#payment detail
class PaymentDetail(AdminPermission, View):
    template_name = 'administration/payment-detail.html'

    def get(self, request, payment_id):

        payment = get_object_or_404(account_model.Payment, pk=payment_id)

        variables = {
            'payment': payment,
        }

        return render(request, self.template_name, variables)


    def commission_sale_calculation(self, referred_payment, referred_percent):
        payable = (referred_payment*referred_percent) / 100

        return payable


    def commission_sale_deploy(self, request, payment):
        sponsor_obj = payment.user.sponsor
        referred_user = payment.user
        referral_membership = payment.membership
        sponsor_membership = sponsor_obj.membership.name


        referred_payment = referral_membership.price

        get_commission = None

        if sponsor_membership == 'free':
            get_commission = self.commission_sale_calculation(referred_payment, 10)
        elif sponsor_membership == 'premium':
            get_commission = self.commission_sale_calculation(referred_payment, 40)
        elif sponsor_membership == 'vip':
            get_commission = self.commission_sale_calculation(referred_payment, 70)



        deploy = account_model.ReferralSaleCommission(user=sponsor_obj, referred_user=referred_user, referred_user_payment=payment, commission=get_commission)
        deploy.save()

        email.sent_commission_email(sponsor_obj, referred_user, referral_membership, get_commission)


    def check_payment(self, params):
        pass


    def post(self, request, payment_id):
        payment = get_object_or_404(account_model.Payment, pk=payment_id)

        payment_user = payment.user

        payment_user_profile = account_model.UserProfile.objects.get(id=payment_user.id)
        payment_membership = payment.membership

        expired_date = payment.expired_time

        #today = datetime.utcnow() + relativedelta(minutes=2)


        if request.POST.get('check_payment') == 'check_payment':
            print(len(payment.paypal_confirmation.ipn_message))


        if request.POST.get('authorize') == 'authorize':
            payment.is_verify = 'authorized'
            payment.save()

            tasks.membership_change.apply_async(args=[payment_user_profile.id, payment_id], eta=expired_date)


            #referral sale commission calculation
            self.commission_sale_deploy(request, payment)



        elif request.POST.get('reject') == 'reject':
            free_membership_obj = account_model.Membershiplevel.objects.get(name='free')
            payment_user_profile.membership = free_membership_obj
            payment_user_profile.payments = None
            payment_user_profile.save()


            payment.is_verify = 'rejected'
            payment.save()

        elif request.POST.get('expired') == 'expired':
            free_membership_obj = account_model.Membershiplevel.objects.get(name='free')
            payment_user_profile.membership = free_membership_obj
            payment_user_profile.package_buy_time = None
            payment_user_profile.save()

            payment.is_verify = 'expired'
            payment.save()

        variables = {
            'payment': payment,
        }

        return render(request, self.template_name, variables)








#module control view
class ModuleControl(AdminPermission, View):
    template_name = 'administration/module-control.html'

    def get(self, request):

        modules = Module.objects.all()

        variables = {
            'modules': modules,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        modules = Module.objects.all()

        module_id = request.POST.get('module_id')
        module_action = request.POST.get('module_action')

        if module_action == 'disable':
            change_state = Module.objects.filter(id=module_id).update(is_active=False)

            module_obj = Module.objects.get(id=module_id)

            lessons = Lesson.objects.filter(module=module_obj)

            for lesson in lessons:
                lesson.is_active = False
                lesson.save()

        if module_action == 'active':
            change_state = Module.objects.filter(id=module_id).update(is_active=True)
            module_obj = Module.objects.get(id=module_id)

            lessons = Lesson.objects.filter(module=module_obj)

            for lesson in lessons:
                lesson.is_active = True
                lesson.save()

        variables = {
            'modules': modules,
        }

        return render(request, self.template_name, variables)


#lesson control view
class LessonControl(AdminPermission, View):
    template_name = 'administration/lesson-control.html'

    def get(self, request):
        modules = Module.objects.all()

        variables = {
            'modules': modules,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#lesson detail view
class LessonDetail(AdminPermission, View):
    template_name = 'administration/lesson-detail.html'

    def get(self, request, module_id):

        modules = Module.objects.filter(id=module_id)

        lessons = Lesson.objects.filter(module=modules).all()

        variables = {
            'modules': modules,
            'lessons': lessons,
        }

        return render(request, self.template_name, variables)

    def post(self, request, module_id):
        modules = Module.objects.filter(id=module_id)
        lessons = Lesson.objects.filter(module=modules).all()

        lesson_id = request.POST.get('lesson_id')
        lesson_action = request.POST.get('lesson_action')

        print(lesson_id, lesson_action)

        if lesson_action == 'disable':
            change_state = Lesson.objects.filter(id=lesson_id).update(is_active=False)

        if lesson_action == 'active':
            change_state = Lesson.objects.filter(id=lesson_id).update(is_active=True)

        variables = {
            'modules': modules,
            'lessons': lessons,
        }

        return render(request, self.template_name, variables)


#affiliate link control
class AffiliateLinkControls(AdminPermission, View):
    template_name = 'administration/affiliate-link-control.html'

    def get(self, request):

        affiliates = AffiliateLinkControl.objects.all()

        variables = {
            'affiliates': affiliates,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        affiliates = AffiliateLinkControl.objects.all()

        link_id = request.POST.get('link_id')
        link_action = request.POST.get('link_action')

        if link_action == 'disable':
            change_state = AffiliateLinkControl.objects.filter(id=link_id).update(is_active=False)

        if link_action == 'active':
            change_state = AffiliateLinkControl.objects.filter(id=link_id).update(is_active=True)

        variables = {
            'affiliates': affiliates,
        }

        return render(request, self.template_name, variables)


#step control
class StepControls(AdminPermission, View):
    template_name = 'administration/step-control.html'

    def get(self, request):

        steps = StepControl.objects.all()

        variables = {
            'steps': steps,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        steps = StepControl.objects.all()

        step_id = request.POST.get('step_id')
        step_action = request.POST.get('step_action')

        if step_action == 'disable':
            change_state = StepControl.objects.filter(id=step_id).update(is_active=False)

        if step_action == 'active':
            change_state = StepControl.objects.filter(id=step_id).update(is_active=True)

        variables = {
            'steps': steps,
        }

        return render(request, self.template_name, variables)



#lesson control view
class AddVideo(AdminPermission, View):
    template_name = 'administration/add-video.html'

    def get(self, request):
        form = forms.VideoLinkForm()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        form = forms.VideoLinkForm(request.POST or None)

        if form.is_valid():
            form.deploy()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)


#pending commission payment
class CommissionPayment(View):
    template_name = 'administration/commission-payout-list.html'

    def get(self, request):

        commissions = account_model.ReferralSaleCommission.objects.filter(is_verified=False).all()

        variables = {
            'commissions': commissions,
        }

        return render(request, self.template_name, variables)



#pending commission payment
class CommissionPaymentDetail(View):
    template_name = 'administration/commission-payout-detail.html'

    def get(self, request, commission_id):
        commission = get_object_or_404(account_model.ReferralSaleCommission, pk=commission_id)

        current_payment_account = home_model.PaymentAccountSetting.objects.filter(user=commission.user)


        variables = {
            'commission': commission,
            'current_payment_account': current_payment_account,
        }

        return render(request, self.template_name, variables)
    def post(self, request, commission_id):
        commission = get_object_or_404(account_model.ReferralSaleCommission, pk=commission_id)

        current_payment_account = home_model.PaymentAccountSetting.objects.filter(user=commission.user)


        if request.POST.get('authorize') == 'authorize':
            commission.is_verified = True
            commission.verified_by = request.user
            commission.save()

            email.sent_commission_email_confirmation(commission.user, commission.referred_user, commission.referred_user_payment.membership, commission.commission)

        variables = {
            'commission': commission,
            'current_payment_account': current_payment_account,
        }

        return render(request, self.template_name, variables)


