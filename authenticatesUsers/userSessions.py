# # authenticatesUsers/sessions.py
#
# class UserSession:
#     def __init__(self, request):
#         self.session = request.session
#         user_info = self.session.get('user_info')
#         if 'user_info' not in request.session:
#             user_info = self.session['user_info'] = {}
#         self.user_info = user_info
#
#     def add_user(self, user):
#         self.user_info = {
#             'user_id': user.id,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#             'phone': user.customer.phone if hasattr(user, 'customer') else ''
#         }
#         self.save()
#
#     def get_user(self):
#         return self.user_info
#
#     def clear_user(self):
#         self.session['user_info'] = {}
#         self.save()
#
#     def save(self):
#         self.session.modified = True
#
