<?php
/**
 * Search endpoint for the AI Server API.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api\Endpoints;

use SS_AI_Image_Search\Api\Client;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Search endpoint class for image search operations.
 */
class SearchEndpoint {

	/**
	 * API Client instance.
	 *
	 * @var Client
	 */
	private Client $client;

	/**
	 * Constructor.
	 *
	 * @param Client $client API Client instance.
	 */
	public function __construct( Client $client ) {
		$this->client = $client;
	}

	/**
	 * Search for images by text query.
	 *
	 * @param string $query Search query text.
	 * @param array  $params Additional search parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function search( string $query, array $params = array() ): Response {
		$endpoint = 'search';

		$data = array(
			'query' => $query,
		);

		// Merge additional parameters.
		$data = array_merge( $data, $params );

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Search for images by image URL.
	 *
	 * @param string $image_url Image URL to search with.
	 * @param array  $params Additional search parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function search_by_image( string $image_url, array $params = array() ): Response {
		$endpoint = 'search/image';

		$data = array(
			'image_url' => $image_url,
		);

		// Merge additional parameters.
		$data = array_merge( $data, $params );

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Search for similar images.
	 *
	 * @param int    $product_id Product ID to find similar images for.
	 * @param array  $params Additional search parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function search_similar( int $product_id, array $params = array() ): Response {
		$endpoint = 'search/similar';

		$data = array(
			'product_id' => $product_id,
		);

		// Merge additional parameters.
		$data = array_merge( $data, $params );

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Get search suggestions.
	 *
	 * @param string $query Partial search query.
	 * @param int    $limit Maximum number of suggestions.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_suggestions( string $query, int $limit = 10 ): Response {
		$endpoint = 'search/suggestions';

		$query_params = array(
			'q'     => $query,
			'limit' => $limit,
		);

		return $this->client->get( $endpoint, $query_params );
	}

	/**
	 * Get search history.
	 *
	 * @param int $limit Maximum number of history items.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_history( int $limit = 50 ): Response {
		$endpoint = 'search/history';

		$query_params = array(
			'limit' => $limit,
		);

		return $this->client->get( $endpoint, $query_params );
	}
}