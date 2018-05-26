package base;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.Response;
import org.json.JSONObject;
import java.util.List;
import java.util.StringTokenizer;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

@Path("/apis")
@Produces("application/json")
public class Principal {
	//private static final long serialVersionUID = 1L;
	
	List<User> lUser = new ArrayList<>();
	List<String> lCorreo = new ArrayList<>();
	
	@GET
	public Response mt_Inicio(){
		JSONObject json = new JSONObject().put("mensaje", "Acceso denegado");
		Response response = Response.ok().entity(json.toString()).build();
		return response;
	}
	
	@Path("/facebook")
	@GET
	public Response mt_Correo(@QueryParam("mail") String correo){
		Response response = null;
		boolean bFlag = false;
		try {
			muestraContenido("C:\\correo.txt");
			JSONObject json = null;
			for (int i = 0; i < lCorreo.size(); i++) {
				if ( lCorreo.get(i).equalsIgnoreCase(correo) ){
					json = new JSONObject().put("valida", true).put("mensaje", "Consulta ok");
					bFlag = true;
					
				}else{
					json = new JSONObject().put("valida", false).put("mensaje", "Consulta ok");
				}
				
				if ( bFlag )
					break;
			}
			
			response = Response.ok().entity(json.toString()).build();
		} catch (Exception e) {
			JSONObject json = null;
			json = new JSONObject();
			json.put("valida", false);
			json.put("mensaje", e.toString());
			response = Response.ok().entity(json.toString()).build();
		}

		return response;
	}
	

    public void muestraContenido(String archivo){
    	try {
            String cadena;
            FileReader f = new FileReader(archivo);
            BufferedReader b = new BufferedReader(f);
            
            while((cadena = b.readLine())!=null) {
            	StringTokenizer token = new StringTokenizer(cadena,";");
                lCorreo.add(token.nextToken());
            }
            b.close();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
  
    }	
}