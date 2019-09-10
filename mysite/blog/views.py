from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.utils import timezone
from blog.forms import PostForm

def post_list(request):
    posts =Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk) #사용자에게 공개할때
    return render(request, 'blog/post_detail.html', {'post':post})
    
def post_new(request):
    # request.method는 현재 이 함수를 실행하기 위해 들어온 요청이
    # POST방식이라면 문자열 "POST"를 , GET방식이라면 문자열 "GET" 출력
    # 따라서, POST 방식인지를 구분부터 해 준다
    if request.method == "POST":
        # form변수에 빈 칸이 채워진 Form 양식을 받아옴
        form = PostForm(request.POST)
        # .is_valid()는 form에서 요청한 자료가 모두 기입되었는지
        # 체크하는 메서드, 만약 모두 기입되지 않았다면 False
        # 모두 기입되었다면 True를 반환한다
        if form.is_valid() :
            # .save()는 아무것도 입력을 안하면 DB에 바로 
            # 데이터를 적재해버리기 때문에 우선 form양식 이외에
            # 작성자, 퍼블리싱 시간을 추가 적재하기 위해 임시로 
            # DB에 올리기만 하기 위해 commit=False
            post = form.save(commit=False)
            # 현재 로그인된 유저를 글쓴이 정보에 저장
            post.author = request.user
            # 퍼블리싱 날짜는 현재 시간으로 저장
            post.published_date = timezone.now()
            # 모든 작업 완료 후 실제 DB에 저장
            post.save()
            # POST방식으로 드러왔으며, 자료 적재도 완전히 끝나면
            # 쓴 글을 확인할 수 있는 상세 페이지로 이동
            # redirect('url패턴', 우아한url변서명=넣을자료)
            return redirect('post_detail', pk=post.pk)
    # 폼 작성시 어떤 양식을 따라갈 것인지 지정
    # 현재 우리가 form.py에 작성한 PostForm을 활용해
    # 품을 자동으로 구성할 예정
    else:
        # get방식으로 들어오는 경우는 자료를 반영하지 않고
        # 그냥 다시 post방식 작성을 유도하기 우해 품으로 
        # 이동시키는 로직 실행
        form = PostForm()
    # render에서는 먼저 템플릿파일 연결 후 폼 정보를 가진
    # form 변수를 같이 넘겨준다
    return render(request, 'blog/post_edit.html', {'form':form})
