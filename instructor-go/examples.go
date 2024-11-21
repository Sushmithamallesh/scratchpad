package main

import (
	"encoding/json"
	"reflect"

	"github.com/invopop/jsonschema"
)

type Schema struct {
	*jsonschema.Schema
	String string
}

type User struct {
	FirstName      string     `json:"first_name"        jsonschema:"title=First Name,description=The first name of the user"            validate:"required"`
	LastName       string     `json:"last_name"         jsonschema:"title=Last Name,description=The last name of the user"              validate:"required"`
	Age            uint8      `json:"age"               jsonschema:"title=Age,description=The age of the user"                          validate:"gte=0,lte=130"`
	Email          string     `json:"email"             jsonschema:"title=Email,description=The email address of the user"              validate:"required,email"`
	Gender         string     `json:"gender"            jsonschema:"title=Gender,description=The gender of the user"                    validate:"oneof=male female prefer_not_to"`
	FavouriteColor string     `json:"favourite_color"   jsonschema:"title=Favourite Color,description=The favourite color of the user"  validate:"iscolor"`
	Addresses      []*Address `json:"addresses"         jsonschema:"title=Addresses,description=The addresses of the user"              validate:"required,dive,required"`
}

type Address struct {
	Street string `json:"street"    jsonschema:"title=Street,description=The street address"    validate:"required"`
	City   string `json:"city"      jsonschema:"title=City,description=The city"                validate:"required"`
	Planet string `json:"planet"    jsonschema:"title=Planet,description=The planet"            validate:"required"`
	Phone  string `json:"phone"     jsonschema:"title=Phone,description=The phone number"       validate:"required"`
}

func main() {
	var user User
	t := reflect.TypeOf(user)

	schema, err := NewSchema(t)
	if err != nil {
		panic(err)
	}
	// print the schema
	println(schema.String)

}
func NewSchema(t reflect.Type) (*Schema, error) {

	schema := jsonschema.ReflectFromType(t)

	str, err := json.MarshalIndent(schema, "", "  ")
	if err != nil {
		return nil, err
	}

	s := &Schema{
		Schema: schema,
		String: string(str),
	}

	return s, nil
}
