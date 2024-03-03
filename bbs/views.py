from django.shortcuts import get_object_or_404, render, redirect
from .forms import BoardForm
from .models import Board

# Create your views here.
def index(request):
    return render(request, 'index.html')

def m_new(request):
    # print(request.user.user_id)
    # 글등록시
    if request.method == 'POST':
        form = BoardForm(request.POST)
        # if form.is_valid():
        #     form.save()
        if form.is_valid():
            BBS = form.save(commit=False)
            BBS.user_id = request.user.user_id
            BBS.save()

        return redirect('bbs:list') 
    
    # 페이지 그냥 들어온경우
    else:
        form = BoardForm()
    return render(request, 'bbs/write.html', {'forms':form})


def list(request):
    articleList = Board.objects.all()
    return render(request, 'bbs/list.html', {'articleList':articleList})


def detail(request, pk):
    article = Board.objects.get(seq=pk)
    return render(request, 'bbs/view.html', {'article':article})

def edit(request, pk):
    edit = Board.objects.get(seq=pk)
    return render(request, 'bbs/edit.html', {'Board':edit})

def update(request, pk):
    # update_Board = Board.objects.get(id=pk)
    # update_Board.title = request.POST['title']
    # update_Board.name = request.POST['writer']
    # update_Board.contents = request.POST['body']
    # # update_Board.pub_date = timezone.now()
    # update_Board.save()
    form = get_object_or_404(Board, seq=pk)
    BBS = BoardForm(request.POST, instance=form)
    if BBS.is_valid():
        aaa = BBS.save(commit=False)
        aaa.save()

    return redirect('bbs:edit', pk=pk )

def delete(request, pk):
    delete_Board = Board.objects.get(id=pk)
    delete_Board.delete()

    return redirect('bbs:list')

def ati(request):
    # print(request.user_id)
    return render(request,'bbs/list.html')