import scrapy
import re

visited_links = set()


def is_secure(link):
	return link is not None and re.search(r'.*uniandes.*',link) is not None

class UniandesSpider(scrapy.Spider):
	
	name = "nephila"
	
	start_urls = [
		'https://uniandes.edu.co/es/programas-facultades/lista-facultades/'
	]
	
	def parse(self,response):
		for link in response.css('.views-field-field-url-caja-list1 a::attr(href)').extract():
			next_page = response.urljoin(link)
			if is_secure(next_page):
				visited_links.add(next_page)
				yield scrapy.Request(next_page, callback=self.process_faculty)

	def process_faculty(self,response):
		for link in response.css('a::attr(href)').extract():
			next_page = response.urljoin(link)
			if is_secure(next_page) and re.search(r'.*profesores.*planta.*',next_page) is not None:
				visited_links.add(next_page)
                                yield scrapy.Request(next_page,callback=self.process_main_teachers)
			elif is_secure(next_page) and re.search(r'.*arqdis.*',next_page) is None and re.search(r'.*profesores$.*',next_page) is not None:
				visited_links.add(next_page)
                                yield scrapy.Request(next_page,callback=self.process_faculty)
	
	def process_main_teachers(self,response):
		for link in response.css('a::attr(href)').extract():
			next_page = response.urljoin(link)
                        if is_secure(next_page) and re.search(r'.*profesores',next_page) is not None:
                                if next_page not in visited_links:
                                        visited_links.add(next_page)
                                        yield scrapy.Request(next_page,callback=self.process_full_time_teachers)

	def process_full_time_teachers(self,response):
		if re.search(r'.*administracion.*',response.url):
			yield {
				'name': response.css('.academia-detail-professor-info').css('h2::text').extract(),
				'mail': response.css('.academia-detail-professor-info').css('.information-header').css('.academia-email::text').extract(),
				'cathedra': False,
				'grades': response.css('.information-degree').css('p::text').extract(),
				'curriculum': '',
				'courses': response.xpath('//div[@id="collapseTwo"]').css('li::text').extract(),
				'facultad': 'Facultad de Administracion'
			}
		elif re.search(r'.*derecho.*',response.url):
			tb_sel = response.css('.content-text').css('table').css('tbody')
                	yield {
                       		'name': tb_sel.css('div').xpath('strong[1]/text()').extract(),
				'mail': '', 
				'cathedra': False,
				'grades': response.css('.content-text').css('.jpane-slider')[0].css('li::text').extract(),
				'curriculum': response.css('.content-text').css('.jpane-slider')[1].css('li::text').extract(),
				'courses': '',
				'facultad': 'Facultad de Derecho'
                	}
		elif re.search(r'.*medicina.*',response.url):
			print ' medicina '
			print response.url
