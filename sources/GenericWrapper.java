public class GenericWrapper<T> {
	private T value;

	public GenericWrapper() {}

	public GenericWrapper(T value) {
		this.value=value;
	}
	
	public void setValue(T value) {
		this.value=value;
	}
	
	public T getValue() {
		return this.value;
	}
}