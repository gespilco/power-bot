package base;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class User {
	private int id = 0;
	private String nombre;
	
	public User() {
	}
	
	public User(String nombre){
		id++;
		this.nombre = nombre;
	}

	
	public int getId() {
		return id;
	}

	public String getNombre() {
		return nombre;
	}

	public void setId(int id) {
		this.id = id;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}	
}
