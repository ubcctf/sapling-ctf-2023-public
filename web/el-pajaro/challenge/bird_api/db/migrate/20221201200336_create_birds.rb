class CreateBirds < ActiveRecord::Migration[7.0]
  def change
    create_table :birds do |t|
      t.string :name
      t.string :classification
      t.string :description
      t.string :image_url

      t.timestamps
    end
  end
end
