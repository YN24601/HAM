from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# class LoginRequiredMixin:
#     """自定义 Mixin：判断用户是否登录"""
#     def dispatch(self, request, *args, **kwargs):
#         if not request.session.get('patient_id'):
#             # 如果未登录，重定向到登录页面user_login
#             return HttpResponseRedirect(reverse('user_login'))
#         return super().dispatch(request, *args, **kwargs)


# class LoginRequiredMixin:
    # """自定义 Mixin：判断用户是否登录"""
    # def dispatch(self, request, *args, **kwargs):
        # if not request.session.get('patient_id'):
        #     if request.is_ajax():
        #         # 如果是 AJAX 请求，返回未登录状态
        #         return JsonResponse({'status': 'unauthenticated', 'redirect_url': reverse('user_login')})
        #     # 如果是普通请求，直接重定向到登录页面
        #     return HttpResponseRedirect(reverse('user_login'))
        # return super().dispatch(request, *args, **kwargs)

class LoginRequiredMixin:
    """自定义 Mixin：判断用户是否登录"""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('patient_id'):
            # 返回一个 HTML 页面，带有 JS 脚本提示未登录并跳转
            login_url = reverse('user_login')
            return HttpResponse(f"""
                <script>
                    alert('您尚未登录，请先登录！');
                    window.location.href = '{login_url}';
                </script>
            """)
        return super().dispatch(request, *args, **kwargs)
