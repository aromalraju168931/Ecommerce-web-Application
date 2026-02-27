from django.shortcuts import render
from .models import Products,Profile,Category,subCategory,VerifiedUser
from django.shortcuts import redirect
import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import UserForm,ProfileForm
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages


def index_page(request):
    if not request.session.get("email"):
        return redirect("verification_part1")

    q = request.GET.get('q', '')
    products_view = Products.objects.all()

    if q:
        products_view = products_view.filter(
            Q(products_name__icontains=q) |
            Q(product_description__icontains=q) |
            Q(subcategory__Category__name__icontains=q) |
            Q(subcategory__name__icontains=q)
        ).distinct()

    pass_val = {
        "q": q,
        "products_view": products_view
    }

    return render(request, 'index_page.html', pass_val)


def otp_login(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Please enter email")
            return redirect("verification_part1")

        # Already verified user
        if VerifiedUser.objects.filter(email=email).exists():
            request.session["email"] = email
            messages.info(request, "Already verified account!")
            return redirect("index_page")

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        request.session["otp"] = otp
        request.session["email"] = email

        send_mail(
            "OTP Verification for MegMar ..! Do not share",
            f"Your OTP is {otp}",
            "example_mail@gmail.com",
            [email],
            fail_silently=False
        )

        messages.success(request, "OTP sent! Check your email.")
        return redirect("verification_part2")

    return render(request, "verfication_part1.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        email = request.session.get("email")

        # Session expired safety check
        if not real_otp or not email:
            messages.error(request, "Session expired. Try again.")
            return redirect("verification_part1")

        if entered_otp == real_otp:

            # Store verified email safely
            VerifiedUser.objects.get_or_create(email=email)

            request.session.pop("otp", None)

            messages.success(request, "Account Verified Successfully!")
            return redirect("index_page")

        else:
            messages.error(request, "Wrong OTP")
            return redirect("verification_part2")

    return render(request, "verification_part2.html")


def addCategory(request):
    if request.method=="POST":
        name=request.POST.get("cat_name")
        Category.objects.create(name=name)
    return render(request,"category.html")

def addsubCategory(request):
    if request.method=="POST":
        name=request.POST.get("sub_name")
        cat_id=request.POST.get("category")
        cate=Category.objects.get(id=cat_id)
        subCategory.objects.create(name=name,Category=cate)

    categ=Category.objects.all()
    return render(request,"subcategory.html",{"categ":categ})

    
def products_upload(request):
    if request.method=="POST":
        products=request.POST.get("name_products")
        desc=request.POST.get("name_desc")
        price=request.POST.get("name_price")
        image=request.FILES.get("name_image")
        discound=request.POST.get("name_discound")
        sub_id=request.POST.get("subcategory")
        subcate=subCategory.objects.get(id=sub_id)

        Products.objects.create(products_name=products,product_description=desc,product_price=price,product_image=image,product_discound=discound,subcategory=subcate)
        messages.success(request,"products uploaded")
        return redirect('index_page')
    categ=Category.objects.all()
    subcateg=subCategory.objects.all()
    
    return render(request,'add_products.html',{"categ":categ,"subcateg":subcateg})


def user_reg(request):
    email = request.session.get("email")

    if not email:
        return redirect("verification_part1")

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Check if user already exists
            if User.objects.filter(username=email).exists():
                return redirect("index_page")

            # Save user
            user = user_form.save(commit=False)
            user.username = email
            user.email = email
            user.save()

            # Save profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "User registered successfully!")
            return redirect("index_page")

        else:
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, "user_reg.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "email": email
    })



def profile_view(request):

    email = request.session.get("email")

    if not email:
        return redirect("verification_part1")

    user = User.objects.filter(username=email).first()

    if not user:
        return redirect("user_reg")

    profile, created = Profile.objects.get_or_create(user=user)

    pro_con = {
        "user": user,
        "profile": profile
    }

    return render(request, "profile_view.html", pro_con)


def list_products(request):
    return render(request,"list_products.html")

def add_to_cart(request,id):
    cart_products=Products.objects.get(id=id)
    cart=request.session.get('cart' ,{})
    
    if str(id) in cart:
        cart[str(id)]+=1
    else:
        cart[str(id)]=1

    request.session['cart']=cart
    messages.success(request,"added to cart")
    return redirect('index_page')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_products = Products.objects.filter(id__in=cart.keys())

    cart_items = []
    grand_total = 0

    for c_p in cart_products:
        qty = int(cart[str(c_p.id)])
        total_price = c_p.product_price * qty
        grand_total += total_price

        cart_items.append({
            "c_p": c_p,
            "quantity": qty,
            "total_price": total_price
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })



def del_cart_items(request,id):
    del_cart=request.session.get('cart',{})
    if str(id) in del_cart:
        del del_cart[str(id)]

    request.session['cart']=del_cart
    return redirect('cart_view')


def update_cart(request,id):
    upcart=request.session.get('cart',{})
    if request.method=="POST":
        qty=int(request.POST.get("qty"))
        if str(id) in upcart:
            upcart[str(id)]=qty
        request.session['cart']=upcart
    return redirect('cart_view')

