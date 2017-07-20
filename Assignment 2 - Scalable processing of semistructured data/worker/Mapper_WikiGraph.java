package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/*This Mapper will emit information of people in the following format:
 * Key ("Lugar, [CIUDAD]"), Value("Persona, [NOMBRE], [FECHA_DE_NACIMIENTO]")
 * Thus, in the shuffle phase, all tuples grouped by place of birth
 * The reducer will receive a list of all people born in one place and emits a String
 * Lugar, [CIUDAD] | Persona, [NOMBRE], [FECHA_DE_NACIMIENTO]
 */
public class WCMapper extends Mapper<LongWritable, Text, Text, Text> {
	
	@Override
	protected void map(LongWritable key, Text value,
			Context context)
			throws IOException, InterruptedException {		
	    //First we determine the type of the page (Person or City) to extract respective information
		//For now this is limited to extracting Persons
	    String birth_place_pattern = "(birth_place.+)";
		Pattern birthPlacePattern = Pattern.compile(birth_place_pattern);
		Matcher personMatcher = birthPlacePattern.matcher(value.toString());
		//Only people profiles contain a birth_place, so if the regular expression is a match,
		//we have found a person and can extract further info
	    if (personMatcher.find()) {
	    	//Define base information we will later pass on, if no city of date is found, None is returned
	    	String person_name = "";
	    	String person_city = "None";
	    	String person_date = "None";
	    	//First we extract just the line with birth place
	    	String birth_place = personMatcher.group(1);
	    	//Setting regex pattern to find cities of birth or names consisting of up to 4 names
	    	String name_city_pattern = "(=\\s*(\\[\\[\\s?)?)(([A-Z\\.a-zšćáàäüöóòōíìéèńñ]+)( )?(([A-Za-z\\.šćáàäüöōóòíìéèńñ]+)( )?){0,4})";
	    	Pattern nameCityPattern = Pattern.compile(name_city_pattern);
	    	Matcher cityMatcher = nameCityPattern.matcher(birth_place);
	    	//Setting the person_city variable if birth_place has been found
	    	if (cityMatcher.find()){
	    		person_city = cityMatcher.group(3);
	    		//System.out.println("The person lives in " + person_city);
	    	}	    	
	    	//Extracting line containing the person's name
	    	String person_name_pattern = "(\\|.{1}(birth_)?name.+)";
			Pattern namePattern = Pattern.compile(person_name_pattern);
			Matcher nameLineMatcher = namePattern.matcher(value.toString());
			//If line is found and a name is found within the line, we set the person_name variable
			if (nameLineMatcher.find()){
				String name = nameLineMatcher.group(1);
				Matcher nameMatcher = nameCityPattern.matcher(name);
				if (nameMatcher.find()){
					person_name += nameMatcher.group(3);
					System.out.println("Person is called" + person_name);
				}
			}
			//Finally we extract the line with birth date. If it is found and within
			//the line the regex pattern matches the date, we construct the person_date string
	    	String person_date_pattern = "(\\|.{1}birth_date.+)";
			Pattern datePattern = Pattern.compile(person_date_pattern);
			Matcher dateMatcher = datePattern.matcher(value.toString());
			if (dateMatcher.find()){
				//Extract year, month, and day from line
				String date_line = dateMatcher.group(1);
				String date_pattern = "(\\d{1,4})\\|(\\d{1,2})\\|(\\d{1,2})";
				Pattern datePattern2 = Pattern.compile(date_pattern);
				Matcher dateMatcher2 = datePattern2.matcher(date_line);
				if (dateMatcher2.find()){
				person_date = dateMatcher2.group(1) + "-" + dateMatcher2.group(2) + "-" + dateMatcher2.group(3);	
				}				
			}
			if (!person_name.isEmpty()){
				context.write(new Text("Lugar, " + person_city), new Text("Persona, " + person_name + ", " + person_date));
			}
	     //IF no person is found, we ignore the read page
	     }else {
	        //System.out.println("NO MATCH");
	     }

	}
}
