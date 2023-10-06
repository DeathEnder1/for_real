
# @login_required(login_url='login')
# def setting(request, id):
#     articles=Blog1.objects.get(id=id)
#     if request.method=="POST":
#         articles.delete()
#         return redirect('/display')
#     return render(request, 'delete.html', {'articles':articles})