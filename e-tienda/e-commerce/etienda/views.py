from django.shortcuts import HttpResponse, render, redirect
from .models import ProductManager, save_image_and_get_path
from .forms import ProductForm
from django.contrib import messages
import logging
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)

def index(request):
    logger.info('La página principal ha sido accedida')
    return render(request, 'etienda/base.html')

def landing_page(request):
    try:
        products = list(ProductManager.get_12_random_products())
        logger.info('Mostrando la página de aterrizaje con productos aleatorios')
        if not products:
            logger.warning('No se encontraron productos aleatorios')
            messages.warning(request, 'There was an error loading the landing page. Try again later.')
    except Exception as e:
        logger.error('Error al obtener productos aleatorios: %s', e)
    return render(request, 'etienda/landing_page.html', {'products': products})

def search(request):
    query = request.GET.get('query')
    if not query:
        logger.warning('Intento de búsqueda sin término de búsqueda')
        return render(request, 'etienda/search_results.html', {'error_message': 'You must enter a search term'})
    
    products = list(ProductManager.get_products_with_keyword_in_name(query))
    if not products:
        logger.info('Búsqueda sin resultados para la consulta: %s', query)
        return render(request, 'etienda/search_results.html', {'error_message': 'No products found with that name'})

    logger.info('Resultados de la búsqueda para la consulta: %s', query)
    return render(request, 'etienda/search_results.html', {'products': products})

def category_view(request, category):
    formatted_category = category.replace("-", "").replace("clothing", "'s clothing")
    try:
        products = list(ProductManager.get_products_by_category(formatted_category))
        if not products:
            logger.info('No se encontraron productos para la categoría: %s', formatted_category)
            return render(request, 'etienda/category_results.html', {'error_message': 'No products found for that category'})
        
        logger.info('Mostrando productos para la categoría: %s', formatted_category)
    except Exception as e:
        logger.error('Error al buscar productos por categoría: %s', e)
        return render(request, 'etienda/category_results.html', {'error_message': 'There was an error searching for products by category'})
    
    context = {
        'category': formatted_category,
        'products': products
    }
    return render(request, 'etienda/category_results.html', context)

def new_product_form_view(request):
    if not request.user.is_staff:
        logger.warning('Intento de acceso a formulario de nuevo producto sin permisos')
        return render(request, 'etienda/new_product_form.html', {'error_message': 'You must be logged in as staff to access this page'})

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form_data = form.cleaned_data
                if 'image' in form_data and form_data['image']:
                    form_data['image'] = save_image_and_get_path(form_data['image'])

                ProductManager.add_product_to_collection(form_data)
                messages.success(request, 'Product added successfully.')
                logger.info('Nuevo producto agregado con éxito')
                return redirect('etienda:new_product_form_view')
            except Exception as e:
                logger.error('Error al agregar el producto: %s', e)
                messages.error(request, 'An error occurred while adding the product.')
        else:
            logger.warning('Intento de agregar producto con formulario inválido')
            messages.warning(request, 'There was an error adding the product. Check the form and try again.')
    else:
        form = ProductForm()
        logger.debug('Formulario de nuevo producto cargado')

    return render(request, 'etienda/new_product_form.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        logger.warning('Intento de inicio de sesión con sesión iniciada')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('Inicio de sesión exitoso')
            return redirect('etienda:landing_page')
        else:
            logger.warning('Intento de inicio de sesión fallido')
            return render(request, 'accounts/login.html', {'error_message': 'Invalid username or password'})
    
    return render(request, 'accounts/login.html')

def consulta_1(request):
    response = HttpResponse(ProductManager.get_products_in_price_range_by_category("electronics", 100, 200))
    return response

def consulta_2(request):
    response = HttpResponse(ProductManager.get_products_with_keyword_in_description('pocket'))
    return response

def consulta_3(request):
    response = HttpResponse(ProductManager.get_products_with_rating_above(4))
    return response

def consulta_4(request):
    response =  HttpResponse(ProductManager.get_men_cloting_sorted_by_rating())
    return response

def consulta_5(request):
    response = HttpResponse(ProductManager.get_total_revenue())
    return response

def consulta_6(request):
    response = HttpResponse(ProductManager.get_total_revenue_by_category())
    return response

def consulta_7(request):
    response = HttpResponse(ProductManager.get_products_by_category('men\'s clothing'))
    return response

def consulta_8(request):
    response = HttpResponse(ProductManager.get_products_with_keyword_in_name('shirt'))
    return response