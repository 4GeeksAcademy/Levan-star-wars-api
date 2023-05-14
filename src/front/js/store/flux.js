const getState = ({ getStore, getActions, setStore }) => {
	return {
	  store: {
		users: [],
		people: [],
		favorites: [],
	  },
	  actions: {
		getAllUsers: async () => {
		  const response = await fetch('/users');
		  const data = await response.json();
		  setStore({ users: data });
		},
		createUser: async (email, password, is_active) => {
		  const response = await fetch('/users', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password, is_active }),
		  });
		  const data = await response.json();
		  setStore((prevStore) => {
			return { ...prevStore, users: [...prevStore.users, data] };
		  });
		},
		getUserFavorites: async (userId) => {
		  const response = await fetch(`/users/${userId}/favorites`);
		  const data = await response.json();
		  setStore({ favorites: data });
		},
		getAllPeople: async () => {
		  const response = await fetch('/people');
		  const data = await response.json();
		  setStore({ people: data });
		},
		createPerson: async (name, gender, height, mass, homeworld) => {
		  const response = await fetch('/people', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, gender, height, mass, homeworld }),
		  });
		  const data = await response.json();
		  setStore((prevStore) => {
			return { ...prevStore, people: [...prevStore.people, data] };
		  });
		},
		getPersonById: async (personId) => {
		  const response = await fetch(`/people/${personId}`);
		  const data = await response.json();
		  setStore((prevStore) => {
			return { ...prevStore, people: [data] };
		  });
		},
	  },
	};
  };
  
  export default getState;